from enum import Enum
from typing import Optional
from cdk_auto_platform.build.vpc_cidr_builder import VpcCidrBuilder
from cdk_auto_platform.models.environments.app_environment import AppEnvironment
from cdk_auto_platform.models.blueprints.ecs_fargate_blueprint import (
    EcsFargateBlueprint,
)

from cdk_auto_platform.models.blueprints.database_blueprint import DatabaseBlueprint


from cdk_auto_platform.models.tenants.infrastructure_types import InfrastructureTypes
from cdk_auto_platform.models.vpc.ip_ranges_types import IpPrivateRanges
from cdk_auto_platform.models.vpc.prefix_list_cidr import PrefixListCidr


class TenantBase:
    def __init__(
        self,
        company: str,
        product: Enum,
        principal_dns: str,
        infrastructure_type: InfrastructureTypes,
        aws_account: Optional[str] = None,
        aws_region: Optional[str] = None,
        certificate_arn: Optional[str] = None,
        ip_private_ranges: Optional[IpPrivateRanges] = None,
        prefix_list_cidrs: Optional[list[PrefixListCidr]] = None,
    ):
        self._principal_dns = principal_dns
        self.company = company
        self.product = product
        self.AWS_ACCOUNT = aws_account
        self.AWS_REGION = aws_region
        self.federated_dns = f"{self.product.value}.{self._principal_dns}"
        self.private_dns = f"internal.{self.federated_dns}"
        self.certificate_arn = certificate_arn
        self._infrastructure_type = infrastructure_type
        self.ip_private_ranges = ip_private_ranges
        self.validate_ip_private_ranges()
        self.prefix_list_cidrs = prefix_list_cidrs
        self.validate_prefix_list_cidrs()
        if self._infrastructure_type != InfrastructureTypes.SERVERLESS:
            self.vpc_cidr = VpcCidrBuilder.build(self.ip_private_ranges)  # type: ignore

    def validate_ip_private_ranges(self):
        if self._infrastructure_type != InfrastructureTypes.SERVERLESS:
            if self.ip_private_ranges is None:
                raise ValueError(
                    "ip_private_ranges must be defined for "
                    f"{self._infrastructure_type.value} infrastructure type"
                )

    def validate_prefix_list_cidrs(self):
        if self._infrastructure_type != InfrastructureTypes.SERVERLESS:
            if self.prefix_list_cidrs is not None:
                for prefix_list_cidr in self.prefix_list_cidrs:
                    prefix_list_cidr.validate_cidr()
            else:
                raise ValueError(
                    "prefix_list_cidrs must be defined for "
                    f"{self._infrastructure_type.value} infrastructure type"
                )

    def _builder_blueprints(
        self,
        ecs_fargate_blueprints: Optional[dict[Enum, EcsFargateBlueprint]] = None,
        rds_blueprints: Optional[dict[Enum, DatabaseBlueprint]] = None,
    ):
        if self._infrastructure_type == InfrastructureTypes.ECS_FARGATE_RDS:
            self._ecs_fargate_blueprints = ecs_fargate_blueprints
            self._rds_blueprints = rds_blueprints
        elif self._infrastructure_type == InfrastructureTypes.ECS_EC2_RDS:
            raise NotImplementedError(
                f"{InfrastructureTypes.ECS_EC2_RDS.value} " "is not implemented yet"
            )
        elif self._infrastructure_type == InfrastructureTypes.RDS_ONLY:
            self._rds_blueprints = rds_blueprints

    @property
    def ecs_fargate_blueprints(self):
        if (
            not hasattr(self, "_ecs_fargate_blueprints")
            or self._ecs_fargate_blueprints is None
        ):
            raise ValueError("ECS Fargate blueprints are not defined for this tenant")
        return self._ecs_fargate_blueprints

    @property
    def rds_blueprints(self):
        if not hasattr(self, "_rds_blueprints") or self._rds_blueprints is None:
            raise ValueError("RDS blueprints are not defined for this tenant")
        return self._rds_blueprints

    def local(self):
        self.environment = AppEnvironment.LOCAL

        return self

    def dev(self):
        self.environment = AppEnvironment.DEV

        return self

    def uat(self):
        self.environment = AppEnvironment.UAT

        return self

    def prod(self):
        self.environment = AppEnvironment.PROD

        return self
