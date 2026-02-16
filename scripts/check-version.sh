#!/bin/bash
# Version Checker Script
# Verifies that version numbers are consistent across files

set -e

cd "$(dirname "$0")/../src"

echo "🔍 Checking version consistency..."
echo ""

# Get version from pyproject.toml (look for the actual version, not templates)
PYPROJECT_VERSION=$(grep '^current_version = ' pyproject.toml | head -1 | cut -d'"' -f2)
echo "📄 pyproject.toml version: $PYPROJECT_VERSION"

# Get version from __init__.py if it exists
if [ -f "cdk_auto_platform/__init__.py" ]; then
    INIT_VERSION=$(grep '^__version__ = ' cdk_auto_platform/__init__.py | head -1 | cut -d'"' -f2)
    echo "📄 __init__.py version:    $INIT_VERSION"
    
    if [ "$PYPROJECT_VERSION" = "$INIT_VERSION" ]; then
        echo ""
        echo "✅ Versions match! Current version: $PYPROJECT_VERSION"
        exit 0
    else
        echo ""
        echo "❌ Version mismatch detected!"
        echo "   pyproject.toml: $PYPROJECT_VERSION"
        echo "   __init__.py:    $INIT_VERSION"
        exit 1
    fi
else
    echo "⚠️  __init__.py not found"
    echo ""
    echo "Current version (from pyproject.toml): $PYPROJECT_VERSION"
fi
