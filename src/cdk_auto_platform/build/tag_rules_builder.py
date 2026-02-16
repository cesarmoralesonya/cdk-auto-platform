from aws_cdk import Stack, Tags

from cdk_auto_platform.models.tenants.tenant_base import TenantBase


class TagRulesBuilder:
    @staticmethod
    def _build_tag_rules(
            stack: Stack,
            tenant: TenantBase):
        required_tags = {
            'company': tenant.company,
            'product': tenant.product.value,
            'environment': tenant.environment.value
        }

        for key, value in required_tags.items():
            Tags.of(stack).add(key, value)
