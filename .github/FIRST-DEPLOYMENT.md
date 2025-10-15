# First Deployment Checklist

Use this checklist for your first deployment after implementing the CI/CD pipeline.

## ✅ Pre-Deployment Checklist

### 1. Verify Files

- [X] `.github/workflows/build.yml` exists
- [X] `.github/workflows/publish.yml` exists
- [X] `.github/workflows/release.yml` exists
- [X] `src/iden_q_auto_platform/__init__.py` exists with `__version__`
- [X] `src/MANIFEST.in` exists
- [X] `scripts/build-local.sh` is executable
- [X] `scripts/check-version.sh` is executable
- [X] `README.md` is updated

### 2. Version Consistency

```bash
# Run the version checker
./scripts/check-version.sh
```

- [X] Versions match in both files
- [X] Current version is `1.0.45`

### 3. Local Build Test

```bash
# Build the package locally
./scripts/build-local.sh
```

- [X] Build completes without errors
- [X] `twine check` passes
- [X] Package files are created in `src/dist/`

### 4. Repository Settings

- [X] GitHub Actions are enabled
- [X] Actions have read/write permissions
  - Go to: Settings → Actions → General → Workflow permissions
  - Select: "Read and write permissions"

## 🚀 Deployment Steps

### Step 1: Monitor Build Workflow

```bash
# Watch the build workflow
gh run watch

# Or view in browser
open "https://github.com/iden-q/iden-q-auto-platform/actions"
```

- [X] Build workflow started
- [X] Python 3.11 build passed
- [X] Python 3.12 build passed
- [X] No errors in logs

### Step 3: Create First Release

#### Option A: Using Release Workflow (Recommended)

```bash
# Trigger release workflow with patch bump
gh workflow run release.yml -f bump_type=patch -f create_release=true

# Monitor the workflow
gh run watch
```

#### Option B: Manual Tag

```bash
# Create and push tag
git tag 1.0.46
git push origin 1.0.46

# Monitor the workflow
gh run watch
```

- [ ] Release workflow triggered
- [ ] Version bumped successfully
- [ ] Publish workflow triggered
- [ ] Package built
- [ ] Package published to GitHub Packages
- [ ] GitHub Release created

### Step 4: Verify Publication

```bash
# Check releases
gh release list

# Check packages (browser)
open "https://github.com/iden-q/iden-q-auto-platform/packages"
```

- [ ] Release appears in GitHub Releases
- [ ] Package appears in GitHub Packages
- [ ] Release notes are generated
- [ ] Artifacts are attached to release

## 🧪 Post-Deployment Testing

### Test 1: Install from GitHub Packages

```bash
# Create a test environment
mkdir -p /tmp/test-iden-q
cd /tmp/test-iden-q
python3.12 -m venv venv
source venv/bin/activate

# Set up authentication (replace with your token)
export GITHUB_TOKEN="your_personal_access_token"

# Install the package
pip install \
  --index-url "https://__token__:${GITHUB_TOKEN}@pypi.pkg.github.com/iden-q/iden-q-auto-platform/simple/" \
  iden_q_auto_platform

# Verify installation
python -c "import iden_q_auto_platform; print(iden_q_auto_platform.__version__)"
```

- [ ] Package installs successfully
- [ ] Version number is correct
- [ ] No import errors

### Test 2: Verify Package Contents

```bash
# In the test environment
python -c "import iden_q_auto_platform; print(dir(iden_q_auto_platform))"

# Check if main modules are accessible
python -c "from iden_q_auto_platform.models import *; print('Models imported')"
```

- [ ] Package contents are correct
- [ ] Main modules are importable
- [ ] No missing dependencies

### Test 3: Local Installation Test

```bash
# Back in your project directory
cd /path/to/iden-q-auto-platform
source .venv/bin/activate

# Install in editable mode
cd src
pip install -e .

# Test
python -c "import iden_q_auto_platform; print(iden_q_auto_platform.__version__)"
```

- [ ] Editable install works
- [ ] Version is correct
- [ ] Package is functional

## 📋 Troubleshooting

### Build Workflow Fails

```bash
# View the logs
gh run list --workflow=build.yml --limit 1
gh run view --log
```

**Common issues:**

- Missing dependencies in `pyproject.toml`
- Python version incompatibility
- Syntax errors in workflow files

### Publish Workflow Fails

```bash
# View the logs
gh run view --log
```

**Common issues:**

- Missing workflow permissions
- Version already exists
- Authentication issues

### Package Not Found

**Check:**

- Package visibility (public vs private)
- Authentication token has `read:packages` scope
- Correct repository URL in pip command

### Version Mismatch

```bash
# Fix version mismatch
cd src

# Edit both files to match
# pyproject.toml: current_version = "1.0.45"
# __init__.py: __version__ = "1.0.45"

# Verify
../scripts/check-version.sh
```

## 🎯 Success Criteria

You've successfully deployed when:

- ✅ Build workflow passes on main branch
- ✅ Release workflow creates new version
- ✅ Package appears in GitHub Packages
- ✅ GitHub Release is created with artifacts
- ✅ Package can be installed via pip
- ✅ Package imports work correctly
- ✅ Version number is correct everywhere

## 📚 Next Steps

After successful first deployment:

1. **Update CHANGELOG.md** for the new version
2. **Test the package** in a real project
3. **Set up branch protection** rules if desired
4. **Configure package visibility** (public/private)
5. **Share installation instructions** with team
6. **Document any custom configuration** needed
7. **Set up scheduled workflows** if needed (e.g., weekly builds)

## 🔄 Regular Release Process

For subsequent releases:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main

# Wait for build to pass
gh run watch

# Create release
gh workflow run release.yml -f bump_type=patch  # or minor/major

# Verify
gh release list
```

## 📞 Getting Help

If you encounter issues:

1. Check workflow logs: `gh run view --log`
2. Review documentation in `.github/README.md`
3. Check the architecture diagram in `.github/ARCHITECTURE.md`
4. Review the troubleshooting guide in `.github/CI-CD-GUIDE.md`

---

**Good luck with your first deployment!** 🚀

Remember: Test locally first with `./scripts/build-local.sh`
