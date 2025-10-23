"""
iden_q_auto_platform - AWS CDK Platform Extension

This CDK extension provides a platform for building CDK applications.
"""

__version__ = "1.0.53"
__author__ = "Cesar Morales"
__email__ = "me@cesarmoralesonya.es"

# Expose main components
from iden_q_auto_platform.build import *  # noqa
from iden_q_auto_platform.models import *  # noqa
from iden_q_auto_platform.modules import *  # noqa
from iden_q_auto_platform.packages import *  # noqa
from iden_q_auto_platform.stacks import *  # noqa

__all__ = ["__version__", "__author__", "__email__"]
