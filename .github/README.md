# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the `cdk_auto_platform` Python package.

## Workflows

### 1. Build and Test (`build.yml`)

**Trigger:** Push to `main` or `develop` branches, and pull requests

**Purpose:** Validates that the package can be built successfully across multiple Python versions.

**What it does:**

- Runs on Python 3.11 and 3.12
- Installs dependencies
- Builds the package
- Validates the package with `twine check`
- Uploads build artifacts

### 2. Create Release (`release.yml`)

**Trigger:** Manual workflow dispatch only

**Purpose:** Automates version bumping, PyPI publishing, and GitHub release creation.

**What it does:**

- Bumps the version (patch/minor/major) using `bump-my-version`
- Commits and tags the new version
- Builds the Python package (wheel and source distribution)
- Publishes to PyPI using Trusted Publishing (OIDC)
- Creates a GitHub Release with the built distributions attached

**How to use:**

1. Go to Actions > Create Release
2. Click "Run workflow"
3. Select bump type (patch, minor, or major)
4. Click "Run workflow"

**Or via CLI:**

```bash
gh workflow run release.yml -f bump_type=patch -f create_release=true
```

**Example:**

- Current version: `1.0.45`
- Bump type: `patch`
- New version: `1.0.46`

## Setting up Package Distribution

### PyPI Publishing with Trusted Publishing

The workflow uses PyPI Trusted Publishing (OIDC) for secure, token-free publishing:

1. **No API tokens**: Uses OpenID Connect for authentication
2. **Secure**: No secrets to manage or rotate
3. **Simple**: Works automatically once configured

### Configuring PyPI Trusted Publishing

1. Go to https://pypi.org/manage/account/publishing/
2. Add a new "pending publisher" with:
   - **PyPI Project Name:** `cdk-auto-platform`
   - **Owner:** `cesarmoralesonya`
   - **Repository name:** `cdk-auto-platform`
   - **Workflow name:** `release.yml`
   - **Environment name:** (leave empty)
3. Click "Add"

### Installing Published Packages

#### Method 1: From PyPI (Recommended)

```bash
# Install latest version
pip install cdk-auto-platform

# Install specific version
pip install cdk-auto-platform==1.0.58
```

#### Method 2: Direct URL from GitHub Release

```bash
pip install https://github.com/cesarmoralesonya/cdk-auto-platform/releases/download/1.0.58/cdk_auto_platform-1.0.58-py3-none-any.whl
```

#### Method 3: Using requirements.txt

```text
# requirements.txt
cdk-auto-platform==1.0.58
```

## Version Management

The project uses `bump-my-version` for version management. The version is stored in two places:

- `src/pyproject.toml` (field: `tool.bumpversion.current_version`)
- `src/cdk_auto_platform/__init__.py` (variable: `__version__`)

### Manual Version Bump

If you need to bump the version manually:

```bash
cd src
pip install bump-my-version
bump-my-version bump patch  # or minor, or major
git push origin main --follow-tags
```

## Troubleshooting

### PyPI publishing fails

Check:

1. Trusted Publishing is configured correctly on PyPI
2. The workflow name in PyPI matches `release.yml`
3. The repository owner and name are correct

### Build failures

Check:

1. Python version compatibility (3.11+)
2. All dependencies are correctly specified in `pyproject.toml`
3. The package structure follows Python packaging standards

### Version conflicts

If you see version conflicts:

1. Ensure `pyproject.toml` and `__init__.py` have matching versions
2. Check that tags are properly pushed to GitHub
3. Verify no duplicate versions exist on PyPI

## Additional Resources

- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
