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

**Purpose:** Builds and publishes the package as GitHub Release artifacts.

**What it does:**

- Builds the Python package (wheel and source distribution)
- Validates the package with `twine check`
- Creates a GitHub Release with the built distributions attached
- Uploads package artifacts for download

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

- Bumps the version (patch/minor/major) using `bump-my-version`
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

## Setting up Package Distribution

### Package Distribution via GitHub Releases

The workflows automatically publish packages as GitHub Release artifacts. This approach:

1. **No authentication needed**: Anyone can download releases
2. **Simple installation**: Direct pip install from GitHub URLs
3. **Version tracking**: Each release is clearly versioned and tagged
4. **No additional setup**: Works out of the box with `GITHUB_TOKEN`

### Installing Published Packages

To install the package from GitHub Releases:

### Method 1: Direct URL (Recommended)

```bash
# Install latest release (replace version number)
pip install https://github.com/iden-q/iden-q-auto-platform/releases/download/1.0.46/iden_q_auto_platform-1.0.46-py3-none-any.whl
```

### Method 2: Download and Install

```bash
# Download from releases page
# https://github.com/iden-q/iden-q-auto-platform/releases

# Install locally
pip install ./iden_q_auto_platform-1.0.46-py3-none-any.whl
```

### Method 3: Using requirements.txt

```text
# requirements.txt
iden_q_auto_platform @ https://github.com/iden-q/iden-q-auto-platform/releases/download/1.0.46/iden_q_auto_platform-1.0.46-py3-none-any.whl
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

The project uses `bump-my-version` for version management. The version is stored in two places:

- `src/pyproject.toml` (field: `tool.bumpversion.current_version`)
- `src/iden_q_auto_platform/__init__.py` (variable: `__version__`)

### Manual Version Bump

If you need to bump the version manually:

```bash
cd src
pip install bump-my-version
bump-my-version bump patch  # or minor, or major
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
