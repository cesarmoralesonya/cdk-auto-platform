#!/usr/bin/env python3

# Example CDK App for Morales Corp Tenant
# -*- coding: utf-8 -*-

"""
Example CDK App for Morales Corp Tenant
This script sets up the AWS CDK application for the Morales Corp tenant.
"""

from aws_cdk import App, Environment
from tenants.example import TenantExample
from stacks.playground_stack.component import PlaygroundStack


app: App = App()

# region tenants
tenant_example = TenantExample()
# endregion

# region tenant-stacks
tenant_example_playground_stack = PlaygroundStack(
    app,
    tenant_example.prod(),
    env=Environment(
        account=tenant_example.AWS_ACCOUNT, region=tenant_example.AWS_REGION
    ),
)
# endregion

app.synth()  # type: ignore
