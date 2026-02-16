#!/bin/bash
# Local Package Build and Test Script
# This script helps you build and test the package locally before publishing

set -e

echo "🔧 cdk_auto_platform - Local Build and Test"
echo "================================================"

# Change to src directory
cd "$(dirname "$0")/../src"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install --upgrade pip build twine

# Build the package
echo "🏗️  Building package..."
python -m build

# Check the package
echo "✅ Checking package with twine..."
twine check dist/*

# List built files
echo ""
echo "📋 Built files:"
ls -lh dist/

# Extract version
VERSION=$(grep 'current_version = ' pyproject.toml | sed 's/.*current_version = "\(.*\)"/\1/')
echo ""
echo "📌 Package version: $VERSION"

# Show package contents
echo ""
echo "📦 Package contents (sample):"
tar -tzf dist/*.tar.gz | head -20

echo ""
echo "✨ Build completed successfully!"
echo ""
echo "Next steps:"
echo "  - To test locally: pip install dist/cdk_auto_platform-${VERSION}-py3-none-any.whl"
echo "  - To publish: Push a tag (e.g., git tag ${VERSION} && git push origin ${VERSION})"
echo "  - Or use: gh workflow run release.yml"
