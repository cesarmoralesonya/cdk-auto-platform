from enum import Enum
from typing import Optional
from iden_q_auto_platform.models.environments.app_environment import AppEnvironment
from iden_q_auto_platform.models.blueprints.ecs_fargate_blueprint import (
    EcsFargateBlueprint,
)
from iden_q_auto_platform.models.blueprints.database_blueprint import DatabaseBlueprint


class IpPrivateRanges(Enum):
    """
    Range of private IP addresses defined by RFC 1918
        • 10.0.0.0/16 - 65536 IP addresses
        • 172.16.0.0/20 - 4096 IP addresses
        • 192.168.0.0/24 - 256 IP addresses
    """

    LARGE_COMPANY = "10"
    BIG_COMPANY = "172.16"
    SMALL_COMPANY = "192.168"


class InfrastructureTypes(Enum):
    SERVERLESS = "serverless"
    ECS_FARGATE_RDS = "ecs_fargate_rds"
    ECS_EC2_RDS = "ecs_ec2_rds"
    RDS_ONLY = "rds_only"


class PrefixListCidr:
    def __init__(
        self,
        cidr: str,
        description: str,
    ):
        self.CIDR = cidr
        self.DESCRIPTION = description

    def validate_cidr(self):
        if "/16" in self.CIDR:
            raise ValueError("CIDR must not be /16")


class TenantBase:
    def __init__(
        self,
        company: str,
        product: Enum,
        aws_account: str,
        aws_region: str,
        principal_dns: str,
        certificate_arn: str,
        infrastructure_type: InfrastructureTypes,
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
        self.prefix_list_cidrs = prefix_list_cidrs

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

    def dev(self):
        if self.ip_private_ranges == IpPrivateRanges.LARGE_COMPANY:
            self.vpc_cidr = self.ip_private_ranges.value + ".2.0.0/16"
        elif self.ip_private_ranges == IpPrivateRanges.BIG_COMPANY:
            self.vpc_cidr = self.ip_private_ranges.value + ".32.0/20"
        elif self.ip_private_ranges == IpPrivateRanges.SMALL_COMPANY:
            self.vpc_cidr = self.ip_private_ranges.value + ".32.0/24"

        self.environment = AppEnvironment.DEV

        return self

    def uat(self):
        if self.ip_private_ranges == IpPrivateRanges.LARGE_COMPANY:
            self.vpc_cidr = self.ip_private_ranges.value + ".1.0.0/16"
        elif self.ip_private_ranges == IpPrivateRanges.BIG_COMPANY:
            self.vpc_cidr = self.ip_private_ranges.value + ".16.0/20"
        elif self.ip_private_ranges == IpPrivateRanges.SMALL_COMPANY:
            self.vpc_cidr = self.ip_private_ranges.value + ".16.0/24"

        self.environment = AppEnvironment.UAT

        return self

    def prod(self):
        if self.ip_private_ranges == IpPrivateRanges.LARGE_COMPANY:
            self.vpc_cidr = self.ip_private_ranges.value + ".0.0.0/16"
        elif self.ip_private_ranges == IpPrivateRanges.BIG_COMPANY:
            self.vpc_cidr = self.ip_private_ranges.value + ".0.0/20"
        elif self.ip_private_ranges == IpPrivateRanges.SMALL_COMPANY:
            self.vpc_cidr = self.ip_private_ranges.value + ".0.0/24"

        self.environment = AppEnvironment.LIVE

        return self
