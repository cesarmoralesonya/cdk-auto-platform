from aws_cdk import Stack, Tags

from iden_q_auto_platform.models.tenants.tenant_base import TenantBase


class TagRulesBuilder:
    @staticmethod
    def _build_tag_rules(
            stack: Stack,
            tenant: TenantBase):
        required_tags = {
            'company': tenant.COMPANY,
            'product': tenant.PRODUCT.value,
            'environment': tenant.environment.value
        }

        for key, value in required_tags.items():
            Tags.of(stack).add(key, value)
