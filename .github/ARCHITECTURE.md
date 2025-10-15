# CI/CD Pipeline Architecture

```txt
┌─────────────────────────────────────────────────────────────────────────┐
│                         GitHub Actions Workflows                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  1. BUILD AND TEST WORKFLOW (.github/workflows/build.yml)               │
├─────────────────────────────────────────────────────────────────────────┤
│  Trigger: Push to main/develop, Pull Requests                           │
│                                                                          │
│  ┌──────────┐    ┌──────────┐                                          │
│  │ Python   │    │ Python   │                                          │
│  │  3.11    │    │  3.12    │                                          │
│  └────┬─────┘    └────┬─────┘                                          │
│       │               │                                                 │
│       ├───────────────┴─────────────┐                                   │
│       │                             │                                   │
│       ▼                             ▼                                   │
│  Build Package                 Build Package                            │
│  Validate with Twine           Validate with Twine                      │
│  Upload Artifacts              Upload Artifacts                         │
│                                                                          │
│  Result: ✅ Package validated across Python versions                    │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  2. RELEASE WORKFLOW (.github/workflows/release.yml)                    │
├─────────────────────────────────────────────────────────────────────────┤
│  Trigger: Manual (workflow_dispatch)                                    │
│                                                                          │
│  User Input: bump_type (patch/minor/major)                              │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────────────────────────┐                                   │
│  │  Bump Version Job               │                                   │
│  ├─────────────────────────────────┤                                   │
│  │  1. Checkout code               │                                   │
│  │  2. Install bump-my-version     │                                   │
│  │  3. Bump version number         │                                   │
│  │  4. Commit and tag              │                                   │
│  │  5. Push to repository          │                                   │
│  └─────────┬───────────────────────┘                                   │
│            │                                                             │
│            │ Triggers                                                    │
│            ▼                                                             │
│  ┌─────────────────────────────────┐                                   │
│  │  Publish Job                    │                                   │
│  │  (calls publish.yml)            │                                   │
│  └─────────────────────────────────┘                                   │
│                                                                          │
│  Result: ✅ New version created and published                           │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  3. PUBLISH WORKFLOW (.github/workflows/publish.yml)                    │
├─────────────────────────────────────────────────────────────────────────┤
│  Triggers:                                                               │
│  - Tag push (e.g., 1.0.46)                                              │
│  - Manual (workflow_dispatch)                                           │
│  - Called by release.yml (workflow_call)                                │
│                                                                          │
│  ┌─────────────────────────────────┐                                   │
│  │  Extract Version                │                                   │
│  └─────────┬───────────────────────┘                                   │
│            │                                                             │
│            ▼                                                             │
│  ┌─────────────────────────────────┐                                   │
│  │  Build Package                  │                                   │
│  │  - python -m build              │                                   │
│  │  - Creates .whl and .tar.gz     │                                   │
│  └─────────┬───────────────────────┘                                   │
│            │                                                             │
│            ▼                                                             │
│  ┌─────────────────────────────────┐                                   │
│  │  Validate Package               │                                   │
│  │  - twine check dist/*           │                                   │
│  └─────────┬───────────────────────┘                                   │
│            │                                                             │
│            ▼                                                             │
│  ┌─────────────────────────────────┐                                   │
│  │  Publish to GitHub Packages     │                                   │
│  │  - Uses GITHUB_TOKEN            │                                   │
│  └─────────┬───────────────────────┘                                   │
│            │                                                             │
│            ▼                                                             │
│  ┌─────────────────────────────────┐                                   │
│  │  Create GitHub Release          │                                   │
│  │  - Attach distributions         │                                   │
│  │  - Generate release notes       │                                   │
│  └─────────────────────────────────┘                                   │
│                                                                          │
│  Result: ✅ Package published and release created                       │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        Local Development Tools                           │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  scripts/build-local.sh                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  • Clean previous builds                                                │
│  • Install build dependencies                                           │
│  • Build package                                                         │
│  • Validate with twine                                                   │
│  • Show package contents                                                │
│                                                                          │
│  Usage: ./scripts/build-local.sh                                        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  scripts/check-version.sh                                                │
├─────────────────────────────────────────────────────────────────────────┤
│  • Read version from pyproject.toml                                     │
│  • Read version from __init__.py                                        │
│  • Compare and validate                                                  │
│  • Exit 0 if match, 1 if mismatch                                       │
│                                                                          │
│  Usage: ./scripts/check-version.sh                                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         Package Structure                                │
└─────────────────────────────────────────────────────────────────────────┘

src/
├── pyproject.toml                  ← Package metadata & version
├── MANIFEST.in                     ← Distribution file rules
├── CHANGELOG.md                    ← Version history
└── iden_q_auto_platform/
    ├── __init__.py                 ← Version variable
    ├── build/
    ├── models/
    ├── modules/
    ├── packages/
    ├── stacks/
    └── utils/

┌─────────────────────────────────────────────────────────────────────────┐
│                         Version Management                               │
└─────────────────────────────────────────────────────────────────────────┘

Current Version: 1.0.45

Stored in:
├── src/pyproject.toml [tool.bumpversion] current_version = "1.0.45"
└── src/iden_q_auto_platform/__init__.py __version__ = "1.0.45"

Managed by: bump-my-version

Version Flow:
┌──────────────┐
│ Developer    │
│ runs release │
│ workflow     │
└──────┬───────┘
       │
       ▼
┌──────────────────────────┐
│ bump-my-version updates  │
│ both files               │
└──────┬─────────────────── ┘
       │
       ▼
┌──────────────────────┐
│ Git commit & tag     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Trigger publish      │
└──────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         Publishing Flow                                  │
└─────────────────────────────────────────────────────────────────────────┘

Developer Actions:
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  Option 1: Automated Release                                            │
│  ┌────────────────────────────────────────┐                            │
│  │ gh workflow run release.yml            │                            │
│  │   -f bump_type=patch                   │                            │
│  └────────────────────────────────────────┘                            │
│                      │                                                   │
│                      ▼                                                   │
│  [Version bumped, committed, tagged, published]                         │
│                                                                          │
│  Option 2: Manual Tag                                                   │
│  ┌────────────────────────────────────────┐                            │
│  │ git tag 1.0.46                         │                            │
│  │ git push origin 1.0.46                 │                            │
│  └────────────────────────────────────────┘                            │
│                      │                                                   │
│                      ▼                                                   │
│  [Publish workflow triggered]                                           │
│                                                                          │
│  Option 3: Manual Publish                                               │
│  ┌────────────────────────────────────────┐                            │
│  │ gh workflow run publish.yml            │                            │
│  └────────────────────────────────────────┘                            │
│                      │                                                   │
│                      ▼                                                   │
│  [Package published with current version]                               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

GitHub Actions Output:
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  ✅ Package built: iden_q_auto_platform-1.0.46-py3-none-any.whl        │
│  ✅ Source dist:   iden_q_auto_platform-1.0.46.tar.gz                  │
│  ✅ Published to:  GitHub Packages                                      │
│  ✅ Release:       github.com/iden-q/iden-q-auto-platform/releases     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

Installation:
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  pip install \                                                          │
│    --index-url https://USER:TOKEN@pypi.pkg.github.com/...             │
│    iden_q_auto_platform                                                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         Documentation                                    │
└─────────────────────────────────────────────────────────────────────────┘

.github/
├── README.md                      ← Workflow documentation
├── CI-CD-GUIDE.md                 ← Quick reference guide
└── IMPLEMENTATION-SUMMARY.md      ← This summary

README.md (updated)                ← Main project README with badges

┌─────────────────────────────────────────────────────────────────────────┐
│                         Key Features                                     │
└─────────────────────────────────────────────────────────────────────────┘

✅ Automated version management with semantic versioning
✅ Multi-Python version testing (3.11, 3.12)
✅ Package validation before publishing
✅ GitHub Packages publishing
✅ GitHub Releases with artifacts
✅ Reusable workflows
✅ Local testing scripts
✅ Version consistency checking
✅ Comprehensive documentation
✅ Zero additional secrets required

┌─────────────────────────────────────────────────────────────────────────┐
│                         Security                                         │
└─────────────────────────────────────────────────────────────────────────┘

Authentication:
• GITHUB_TOKEN: Automatically provided by GitHub Actions
• Permissions: contents:write, packages:write
• No secrets needed for basic operation

Package Access:
• Public packages: No authentication needed for read
• Private packages: Requires GitHub PAT with read:packages scope

┌─────────────────────────────────────────────────────────────────────────┐
│                         Monitoring                                       │
└─────────────────────────────────────────────────────────────────────────┘

Check workflow status:
• gh run list
• gh run watch
• GitHub Actions UI: github.com/{org}/{repo}/actions

Check packages:
• GitHub Packages UI: github.com/{org}/{repo}/packages

Check releases:
• gh release list
• GitHub Releases UI: github.com/{org}/{repo}/releases
