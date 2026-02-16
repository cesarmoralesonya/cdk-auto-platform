# region: primitives
from enum import Enum
from typing import Optional, Sequence
from constructs import Construct
from pydantic import BaseModel, Field

# endregion

# region: aws-cdk
import aws_cdk as core
from aws_cdk import (
    aws_lambda as lambda_,
    aws_ecr_assets as ecr_assets,
    aws_ecr as ecr,
    aws_ec2 as ec2,
)

# endregion


# region: iden-q-auto-platform
from cdk_auto_platform.models.modules.pug_module import PugModule
from cdk_auto_platform.models.modules.runtime.runtime_function import (
    RuntimeIFunction,
)
from cdk_auto_platform.models.tenants.tenant_base import TenantBase

DEFAULT_MEMORY_SIZE_MB = 128
DEFAULT_EPHEMERAL_STORAGE_SIZE_MB = 512
DEFAULT_TIMEOUT_SECONDS = 3
# endregion


class LambdaPlatform(Enum):
    DOCKER = "docker"
    CODE = "code"


class LambdaConfig(BaseModel):
    memory_size_mb: int = Field(
        default=DEFAULT_MEMORY_SIZE_MB,
        ge=128,
        le=10240,
        description="Memory size in MB for the lambda function",
    )
    ephemeral_storage_size_mb: int = Field(
        default=DEFAULT_EPHEMERAL_STORAGE_SIZE_MB,
        ge=512,
        le=10240,
        description="Ephemeral storage size in MB for the lambda function",
    )
    timeout_seconds: int = Field(
        default=DEFAULT_TIMEOUT_SECONDS,
        ge=3,
        le=900,
        description="Timeout in seconds for the lambda function",
    )


class LambdaParams:
    lambda_name: str
    lambda_platform: LambdaPlatform
    lambda_config: LambdaConfig = LambdaConfig()
    lambda_environment: Optional[dict[str, str]] = {}
    relative_path: Optional[str] = None
    ecr_registry: Optional[str] = None
    exclude: Optional[Sequence[str]] = None
    tenant_vpc: Optional[ec2.IVpc] = None
    vpc_subnets: Optional[ec2.SubnetSelection] = None
    security_groups: Optional[list[ec2.SecurityGroup]] = None
    architecture: lambda_.Architecture = lambda_.Architecture.ARM_64
    tracing: lambda_.Tracing = lambda_.Tracing.ACTIVE

    def __init__(
        self,
        lambda_name: str,
        lambda_platform: LambdaPlatform,
        lambda_config: Optional[LambdaConfig] = None,
        lambda_environment: Optional[dict[str, str]] = None,
        relative_path: Optional[str] = None,
        ecr_registry: Optional[str] = None,
        exclude: Optional[Sequence[str]] = None,
        tenant_vpc: Optional[ec2.IVpc] = None,
        vpc_subnets: Optional[ec2.SubnetSelection] = None,
        security_groups: Optional[list[ec2.SecurityGroup]] = None,
        architecture: lambda_.Architecture = lambda_.Architecture.ARM_64,
        tracing: lambda_.Tracing = lambda_.Tracing.ACTIVE,
    ) -> None:
        self.lambda_name = lambda_name
        self.lambda_platform = lambda_platform
        self.lambda_config = lambda_config or LambdaConfig()
        self.lambda_environment = lambda_environment or {}

        self.relative_path = relative_path
        self.ecr_registry = ecr_registry
        self._validate_source_container()

        self.exclude = exclude
        self.tenant_vpc = tenant_vpc
        self.vpc_subnets = vpc_subnets
        self.security_groups = security_groups
        self.architecture = architecture
        self.tracing = tracing

    def _validate_source_container(self):
        if self.relative_path is None and self.ecr_registry is None:
            raise ValueError(
                "Either 'relative_path' or 'ecr_registry' must be provided"
            )
        if self.relative_path is not None and self.ecr_registry is not None:
            raise ValueError(
                "Only one of 'relative_path' or 'ecr_registry' can be provided"
            )

    def code(self, construct: Construct) -> lambda_.Code:
        if self.relative_path and self.lambda_platform == LambdaPlatform.DOCKER:
            platform = (
                ecr_assets.Platform.LINUX_ARM64
                if self.architecture == lambda_.Architecture.ARM_64
                else ecr_assets.Platform.LINUX_AMD64
            )
            return lambda_.Code.from_asset_image(
                '.',
                exclude=self.exclude,
                asset_name=f"{self.lambda_name}-image",
                platform=platform,
                file=f"./{self.relative_path}/Dockerfile",
            )
        elif self.relative_path and self.lambda_platform == LambdaPlatform.CODE:
            return lambda_.Code.from_asset(
                self.relative_path,
                exclude=self.exclude,
            )
        if self.ecr_registry:
            return lambda_.Code.from_ecr_image(
                repository=ecr.Repository.from_repository_name(
                    construct,
                    f"{self.lambda_name}-ecr-repository",
                    repository_name=self.ecr_registry,
                ),
                tag="latest",
            )

        raise ValueError("Either 'relative_path' or 'ecr_registry' must be provided")


class LambdaPug(PugModule[lambda_.IFunction]):
    def __init__(
        self,
        scope: Construct,
        tenant: TenantBase,
        params: LambdaParams,
    ) -> None:
        TENANT_ENVIRONMENT_LAMBDA_NAME = (
            f"{tenant.company}-{tenant.product.value}-{tenant.environment.value}-{params.lambda_name}"
        )

        function = lambda_.Function(
            scope,
            f"{TENANT_ENVIRONMENT_LAMBDA_NAME}-function",
            function_name=TENANT_ENVIRONMENT_LAMBDA_NAME,
            runtime=(
                lambda_.Runtime.FROM_IMAGE
                if params.lambda_platform == LambdaPlatform.DOCKER
                else lambda_.Runtime.PYTHON_3_12
            ),
            handler=(
                lambda_.Handler.FROM_IMAGE
                if params.lambda_platform == LambdaPlatform.DOCKER
                else "handler.lambda_handler"
            ),
            code=params.code(scope),
            environment=params.lambda_environment,
            memory_size=params.lambda_config.memory_size_mb,
            ephemeral_storage_size=core.Size.mebibytes(
                params.lambda_config.ephemeral_storage_size_mb
            ),
            timeout=core.Duration.seconds(params.lambda_config.timeout_seconds),
            vpc=params.tenant_vpc,
            security_groups=params.security_groups,
            vpc_subnets=params.vpc_subnets,
            architecture=params.architecture,
            tracing=params.tracing,
        )

        assert isinstance(function, RuntimeIFunction)

        super().__init__(function)
