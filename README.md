# iden-q-auto-platform

[![Build and Test](https://github.com/iden-q/iden-q-auto-platform/actions/workflows/build.yml/badge.svg)](https://github.com/iden-q/iden-q-auto-platform/actions/workflows/build.yml)
[![Publish Python Package](https://github.com/iden-q/iden-q-auto-platform/actions/workflows/publish.yml/badge.svg)](https://github.com/iden-q/iden-q-auto-platform/actions/workflows/publish.yml)

IaC platform engineering library based on AWS CDK

## Overview

`iden_q_auto_platform` is a comprehensive CDK extension that provides a platform for building AWS CDK applications with best practices and reusable components.

## Installation

### From GitHub Releases

Download the wheel or source distribution from the [latest release](https://github.com/iden-q/iden-q-auto-platform/releases):

```bash
# Install from wheel
pip install https://github.com/iden-q/iden-q-auto-platform/releases/download/1.0.46/iden_q_auto_platform-1.0.46-py3-none-any.whl

# Or install from source tarball
pip install https://github.com/iden-q/iden-q-auto-platform/releases/download/1.0.46/iden_q_auto_platform-1.0.46.tar.gz
```

### From Source

```bash
git clone https://github.com/iden-q/iden-q-auto-platform.git
cd iden-q-auto-platform/src
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

The package is automatically published via GitHub Actions when:

1. **Automatic**: Push a version tag

   ```bash
   git tag 1.0.46
   git push origin 1.0.46
   ```

2. **Semi-Automatic**: Use the release workflow

   ```bash
   gh workflow run release.yml -f bump_type=patch
   ```

3. **Manual**: Trigger the publish workflow

   ```bash
   gh workflow run publish.yml
   ```

See [.github/README.md](.github/README.md) for detailed workflow documentation.

## Project Structure

```txt
src/iden_q_auto_platform/
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
from iden_q_auto_platform.packages.ecs_service import EcsServicePackage
from iden_q_auto_platform.models.containers import EcsFargateTypes

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
