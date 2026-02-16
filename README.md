# cdk-auto-platform

[![Build and Test](https://github.com/cesarmoralesonya/cdk-auto-platform/actions/workflows/build.yml/badge.svg)](https://github.com/cesarmoralesonya/cdk-auto-platform/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/cdk-auto-platform.svg)](https://pypi.org/project/cdk-auto-platform/)

IaC platform engineering library based on AWS CDK

## Overview

`cdk_auto_platform` is a comprehensive CDK extension that provides a platform for building AWS CDK applications with best practices and reusable components.

## Installation

### From PyPI (Recommended)

```bash
pip install cdk-auto-platform
```

### From GitHub Releases

```bash
pip install https://github.com/cesarmoralesonya/cdk-auto-platform/releases/download/1.0.58/cdk_auto_platform-1.0.58-py3-none-any.whl
```

### From Source

```bash
git clone https://github.com/cesarmoralesonya/cdk-auto-platform.git
cd cdk-auto-platform/src
pip install -e .
```

## Features

- **ECS Fargate Services**: Simplified deployment of containerized applications
- **Database Blueprints**: Pre-configured RDS instances with best practices
- **Monitoring & Alarms**: Built-in CloudWatch dashboards and alarms
- **Networking**: VPC and networking configurations
- **IAM Management**: Federated identity and role management
- **Secrets Management**: Secure handling of application secrets

## Development

### Prerequisites

- Python 3.11 or 3.12
- AWS CDK CLI
- AWS CLI (configured)

### Setup

1. Clone the repository
2. Install dependencies:

```bash
./scripts/install.sh
# Or manually:
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Building the Package

```bash
# Local build and test
./scripts/build-local.sh

# Check version consistency
./scripts/check-version.sh
```

### Publishing

The package is published to PyPI via GitHub Actions:

```bash
# Use the release workflow (recommended)
gh workflow run release.yml -f bump_type=patch -f create_release=true
```

See [.github/README.md](.github/README.md) for detailed workflow documentation.

## Project Structure

```txt
src/cdk_auto_platform/
├── build/              # Build utilities for CDK constructs
├── models/             # Data models and configurations
│   ├── alarms/         # CloudWatch alarm configurations
│   ├── blueprints/     # Service blueprints
│   ├── compute/        # Compute configurations
│   ├── containers/     # Container definitions
│   └── database/       # Database models
├── modules/            # Reusable CDK modules
├── packages/           # High-level packages
│   ├── application_dashboard/
│   ├── application_manager/
│   ├── databases/
│   ├── ecs_service/
│   └── networking/
├── stacks/             # CDK stack definitions
└── utils/              # Utility functions
```

## Usage Example

```python
from aws_cdk import App, Stack
from cdk_auto_platform.packages.ecs_service import EcsServicePackage
from cdk_auto_platform.models.containers import EcsFargateTypes

app = App()
stack = Stack(app, "MyStack")

# Deploy an ECS Fargate service
service = EcsServicePackage(
    stack,
    "MyService",
    fargate_type=EcsFargateTypes.WEB_SERVICE,
    # ... additional configuration
)

app.synth()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) file for details

## Support

For issues and questions:

- GitHub Issues: [iden-q/iden-q-auto-platform/issues](https://github.com/iden-q/iden-q-auto-platform/issues)
- Documentation: [Wiki](https://github.com/iden-q/iden-q-auto-platform/wiki)
