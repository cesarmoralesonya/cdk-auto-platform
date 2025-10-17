# region: primitives
from typing import Any
from constructs import Construct

# endregion

# region: aws-cdk
from aws_cdk import Stack

# endregion

# region: iden-q-auto-platform
from iden_q_auto_platform.build.tag_rules_builder import TagRulesBuilder
# endregion

from iden_q_auto_platform.models.tenants.tenant_base import TenantBase


class PlaygroundStack(
    Stack,
    TagRulesBuilder
):
    def __init__(
            self,
            scope: Construct,
            tenant: TenantBase,
            **kwargs: Any
    ):
        stack_id = f"playground-{tenant.company}-{tenant.product}-{tenant.environment.value}"

        super().__init__(scope, stack_id, **kwargs)
