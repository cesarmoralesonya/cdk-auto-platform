from enum import Enum


class AppEnvironment(Enum):
    LOCAL = "local"
    DEV = "dev"
    UAT = "uat"
    PROD = "prod"
