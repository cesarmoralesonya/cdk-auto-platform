# CI/CD Quick Reference

## 🚀 Publishing Workflows

### Option 1: Automatic Version Bump and Publish (Recommended)

Use the GitHub UI or CLI to trigger a release:

```bash
# Using GitHub CLI
gh workflow run release.yml -f bump_type=patch -f create_release=true

# Options for bump_type:
# - patch: 1.0.45 → 1.0.46 (bug fixes)
# - minor: 1.0.45 → 1.1.0 (new features)
# - major: 1.0.45 → 2.0.0 (breaking changes)
```

**What happens:**

1. ✅ Bumps version in `pyproject.toml` and `__init__.py`
2. ✅ Commits and pushes the changes
3. ✅ Creates a git tag
4. ✅ Builds the package
5. ✅ Publishes to PyPI
6. ✅ Creates a GitHub Release

### Option 2: Manual Tag Push

```bash
# Make sure versions are in sync
./scripts/check-version.sh

# Create and push tag
git tag 1.0.46
git push origin 1.0.46
```

Note: Manual tag pushes do not automatically trigger publishing. Use the release workflow instead.

## 🔍 Checking Build Status

### View Workflow Runs

```bash
# List recent workflow runs
gh run list --workflow=build.yml

# Watch a running workflow
gh run watch
```

### Check Package on GitHub

```bash
# Open packages page
open "https://github.com/iden-q/iden-q-auto-platform/packages"
```

## 🧪 Local Testing Before Publishing

### Build and Test Locally

```bash
# Build the package
./scripts/build-local.sh

# Check version consistency
./scripts/check-version.sh

# Install locally for testing
cd src
pip install -e .

# Or install from dist
pip install dist/cdk_auto_platform-*.whl
```

### Test in Another Project

```bash
# Create test environment
python3.12 -m venv test-env
source test-env/bin/activate

# Install local build
pip install /path/to/iden-q-auto-platform/src/dist/cdk_auto_platform-*.whl

# Test imports
python -c "import cdk_auto_platform; print(cdk_auto_platform.__version__)"
```

## 📦 Installing Published Package

### From PyPI

```bash
# Install latest version
pip install cdk-auto-platform

# Install specific version
pip install cdk-auto-platform==1.0.58
```

### Using requirements.txt

```text
# requirements.txt
cdk-auto-platform==1.0.58
```

## 🐛 Troubleshooting

### Version Mismatch

```bash
# Check versions
./scripts/check-version.sh

# Fix manually if needed
cd src
# Edit pyproject.toml and __init__.py to match
```

### Build Failures

```bash
# Clean and rebuild
cd src
rm -rf dist/ build/ *.egg-info
python -m build

# Check package
twine check dist/*
```

### Authentication Issues

```bash
# Verify GitHub token has correct permissions
# Required scopes: read:packages, write:packages, repo

# Test token
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/packages
```

### Workflow Failures

```bash
# View failed workflow
gh run list --workflow=release.yml --limit 5

# View logs
gh run view WORKFLOW_RUN_ID --log

# Re-run failed workflow
gh run rerun WORKFLOW_RUN_ID
```

## 📋 Common Tasks

### Update Dependencies

```bash
cd src
# Edit requirements.in or pyproject.toml
pip-compile requirements.in
pip install -r requirements.txt
```

### Format Code

```bash
# Run formatting task
# Uses autopep8 and black
source .venv/bin/activate
cd src
autopep8 --in-place --recursive --aggressive --max-line-length 120 cdk_auto_platform
black --line-length 120 cdk_auto_platform
flake8 cdk_auto_platform
```

### Run CDK Commands

```bash
# List stacks
source .venv/bin/activate
PYTHONPATH="src:server/aws/cdk" cdk ls

# Synthesize
PYTHONPATH="src:server/aws/cdk" cdk synth

# Deploy
PYTHONPATH="src:server/aws/cdk" cdk deploy --profile YOUR_PROFILE
```

## 🔐 Required Secrets

The workflows use these secrets (automatically provided):

- `GITHUB_TOKEN`: Automatically provided by GitHub Actions
  - Used for: Creating releases

PyPI publishing uses OpenID Connect (OIDC) Trusted Publishing - no API tokens required.

## 📊 Workflow Matrix

| Workflow | Trigger | Purpose | Duration |
|----------|---------|---------|----------|
| Build and Test | Push/PR | Validate build | ~2-3 min |
| Create Release | Manual | Bump version, publish to PyPI & create release | ~5-7 min |

## 🎯 Best Practices

1. **Always test locally** before triggering workflows
2. **Use release workflow** for version management
3. **Follow semantic versioning**: patch for fixes, minor for features, major for breaking changes
4. **Update CHANGELOG.md** before releasing
5. **Test published package** in a clean environment before announcing
6. **Keep versions in sync** (use check-version.sh)

## 📚 Additional Resources

- [GitHub Actions Workflows](.github/workflows/)
- [Workflow Documentation](.github/README.md)
- [Project README](../README.md)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
