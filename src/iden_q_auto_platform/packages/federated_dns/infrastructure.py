from constructs import Construct

from iden_q_auto_platform.models.tenants.tenant_base import TenantBase

from aws_cdk import (
    aws_ec2 as ec2,
    aws_certificatemanager as acm,
    aws_route53 as route53,
)


"""
The pricing of hosted zone is $0.50 per month for the first 25 hosted zones,
and $0.10 per month for additional hosted zones.
"""


class FederatedDns(Construct):
    def __init__(
        self, scope: Construct, tenant: TenantBase, tenant_vpc: ec2.Vpc, **kwargs
    ):
        super().__init__(scope, "federated-dns", **kwargs)

        FEDERATED_ZONE_ID = (
            f"main-{tenant.company}-{tenant.product}-{tenant.environment.value}-hosted-zone"
        )

        self.main_zone = route53.PublicHostedZone.from_lookup(
            self, FEDERATED_ZONE_ID, domain_name=tenant.federated_dns
        )

        PRIVATE_ZONE_ID = (
            f"main-{tenant.company}-{tenant.product}-{tenant.environment.value}-private-zone"
        )

        self.private_zone = route53.PrivateHostedZone(
            self, PRIVATE_ZONE_ID, vpc=tenant_vpc, zone_name=tenant.private_dns
        )

        CERTIFICATE_ID = f"main-{tenant.company}-{tenant.product}-{tenant.environment.value}-certificate"

        self.certificate = acm.Certificate.from_certificate_arn(
            self, CERTIFICATE_ID, tenant.certificate_arn
        )
