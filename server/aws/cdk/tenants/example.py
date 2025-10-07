from iden_q_auto_platform.models.tenants.tenant_base import (
    IpPrivateRanges,
    PrefixListCidr,
    TenantBase,
    InfrastructureTypes,
)

from enum import Enum

from server.aws.cdk.constants import COMPANY, AWS_DEFAULT_ACCOUNT, AWS_DEFAULT_REGION


class Products(Enum):
    APP = "app"
    API = "api"


class TenantExample(TenantBase):
    """
    Example tenant configuration.
    """

    def __init__(self):
        super().__init__(
            company=COMPANY,
            product=Products.APP,
            aws_account=AWS_DEFAULT_ACCOUNT,
            aws_region=AWS_DEFAULT_REGION,
            principal_dns="example.com",
            certificate_arn="arn:aws:acm:us-west-2:123456789012:certificate/EXAMPLE",
            prefix_list_cidrs=[
                PrefixListCidr(
                    cidr="",
                    description=""
                ),
            ],
            ip_private_ranges=IpPrivateRanges.LARGE_COMPANY,
            infrastructure_type=InfrastructureTypes.SERVERLESS,
        )

    def prod(self):
        return super().prod()

    def uat(self):
        return super().uat()

    def dev(self):
        return super().dev()
