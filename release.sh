#!/bin/bash
# Script to create a new release using jj (Jujutsu)

# Check if version argument is provided
if [ -z "$1" ]; then
    echo "Usage: ./release.sh <version>"
    echo "Example: ./release.sh 0.1.4"
    exit 1
fi

VERSION=$1

echo "🔄 Creating release v$VERSION with jj"

# Update version in pyproject.toml
sed -i "s/version = \"[0-9]*\.[0-9]*\.[0-9]*\"/version = \"$VERSION\"/" pyproject.toml

echo "✅ Updated version to $VERSION"

# Stage the change with jj (jj tracks all changes automatically)
# Just need to describe the change
jj describe -m "Bump version to $VERSION"

echo "✅ Described change"

# Create git tag using jj
jj git tag -r @ "v$VERSION"

echo "✅ Created tag v$VERSION"

# Push to git remote (this triggers GitHub Actions)
jj git push --tags

echo ""
echo "🚀 Release v$VERSION triggered!"
echo "GitHub Actions will now:"
echo "  1. Build the package"
echo "  2. Publish to PyPI"
echo "  3. Create a GitHub release"
echo ""

# Get the GitHub URL from jj
GITHUB_URL=$(jj config get git.push-branch-prefix 2>/dev/null | head -1)
if [ -z "$$GITHUB_URL" ]; then
    echo "📊 Check your GitHub repository Actions tab"
else
    echo "📊 Monitor progress at: https://github.com/$(jj git remote list | head -1 | awk '{print $2}' | sed 's/.*github.com[:/]//;s/.git$//')/actions"
fi
