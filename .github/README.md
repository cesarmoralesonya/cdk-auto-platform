# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the `iden_q_auto_platform` Python package.

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

### 2. Publish Package (`publish.yml`)

**Trigger:**

- Automatically when a version tag is pushed (e.g., `1.0.46`)
- Manually via workflow dispatch

**Purpose:** Builds and publishes the package to GitHub Packages (PyPI-compatible registry).

**What it does:**

- Builds the Python package
- Publishes to GitHub Packages
- Creates a GitHub Release with the built distributions
- Uploads package artifacts

**Manual trigger:**

```bash
# From GitHub UI: Actions > Publish Python Package > Run workflow
# Or using GitHub CLI:
gh workflow run publish.yml
```

### 3. Create Release (`release.yml`)

**Trigger:** Manual workflow dispatch only

**Purpose:** Automates version bumping and package publishing.

**What it does:**

- Bumps the version (patch/minor/major) using `bump2version`
- Commits and tags the new version
- Triggers the publish workflow
- Creates a GitHub release

**How to use:**

1. Go to Actions > Create Release
2. Click "Run workflow"
3. Select bump type (patch, minor, or major)
4. Click "Run workflow"

**Example:**

- Current version: `1.0.45`
- Bump type: `patch`
- New version: `1.0.46`

## Setting up GitHub Packages

### Configure GitHub Packages for Publishing

The workflows are already configured to publish to GitHub Packages. Make sure your repository has the following:

1. **Permissions**: The workflows use `GITHUB_TOKEN` which is automatically provided by GitHub Actions
2. **Package visibility**: Configure in repository settings under Packages

### Installing from GitHub Packages

To install the package from GitHub Packages, users need to:

1. **Create a Personal Access Token (PAT)** with `read:packages` scope
2. **Configure pip** to use GitHub Packages:

```bash
# Add to ~/.pypirc
[distutils]
index-servers =
    github

[github]
repository = https://maven.pkg.github.com/iden-q/iden-q-auto-platform
username = YOUR_GITHUB_USERNAME
password = YOUR_GITHUB_TOKEN
```

1. **Install the package:**

```bash
pip install --index-url https://maven.pkg.github.com/iden-q/iden-q-auto-platform/simple/ iden_q_auto_platform
```

Or using environment variables:

```bash
export PIP_EXTRA_INDEX_URL=https://YOUR_GITHUB_USERNAME:YOUR_GITHUB_TOKEN@maven.pkg.github.com/iden-q/iden-q-auto-platform/simple/
pip install iden_q_auto_platform
```

## Publishing to PyPI (Optional)

If you want to publish to the public PyPI instead of or in addition to GitHub Packages:

1. **Create a PyPI account** at [https://pypi.org](https://pypi.org)
2. **Generate an API token** in your PyPI account settings
3. **Add the token as a GitHub secret** named `PYPI_API_TOKEN`
4. **Update `publish.yml`** to use PyPI:

```yaml
- name: Publish to PyPI
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
  run: |
    cd src
    python -m twine upload dist/*
```

## Version Management

The project uses `bump2version` for version management. The version is stored in two places:

- `src/pyproject.toml` (field: `tool.bumpversion.current_version`)
- `src/iden_q_auto_platform/__init__.py` (variable: `__version__`)

### Manual Version Bump

If you need to bump the version manually:

```bash
cd src
pip install bump2version
bump2version patch  # or minor, or major
git push origin main --follow-tags
```

## Troubleshooting

### Package not found on GitHub Packages

Make sure:

1. The workflow completed successfully
2. The package is set to public or you have access
3. You're using the correct authentication

### Build failures

Check:

1. Python version compatibility (3.11+)
2. All dependencies are correctly specified in `pyproject.toml`
3. The package structure follows Python packaging standards

### Version conflicts

If you see version conflicts:

1. Ensure `pyproject.toml` and `__init__.py` have matching versions
2. Check that tags are properly pushed to GitHub
3. Verify no duplicate versions exist in the registry

## Additional Resources

- [GitHub Packages Documentation](https://docs.github.com/packages)
- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
