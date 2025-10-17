from enum import Enum


class InfrastructureTypes(Enum):
    SERVERLESS = "serverless"
    ECS_FARGATE_RDS = "ecs_fargate_rds"
    ECS_EC2_RDS = "ecs_ec2_rds"
    RDS_ONLY = "rds_only"
