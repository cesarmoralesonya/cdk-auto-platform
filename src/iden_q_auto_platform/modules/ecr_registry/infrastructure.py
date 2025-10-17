# region: primitives
from enum import Enum
from constructs import Construct

# endregion

# region: aws-cdk
import aws_cdk as core
from aws_cdk import aws_ecr as ecr

# endregion

# region iden-q-auto-platform
from iden_q_auto_platform.models.modules.pug_module import PugModule
from iden_q_auto_platform.models.tenants.tenant_base import TenantBase

# endregion


class EcrRegistryPug(PugModule[ecr.Repository]):
    def __init__(self, scope: Construct, tenant: TenantBase, service_type: Enum):
        ECR_REGISTRY_NAME = (
            f"{tenant.company}-{tenant.product}-{tenant.environment.value}-"
            f"{service_type.value}-ecr-registry"
        )

        registry = ecr.Repository(
            scope,
            ECR_REGISTRY_NAME,
            repository_name=ECR_REGISTRY_NAME,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        super().__init__(registry)
