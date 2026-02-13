#!/bin/bash
# Script to create a new release

# Check if version argument is provided
if [ -z "$1" ]; then
    echo "Usage: ./release.sh <version>"
    echo "Example: ./release.sh 0.1.4"
    exit 1
fi

VERSION=$1

# Update version in pyproject.toml
sed -i "s/version = \"[0-9]*\.[0-9]*\.[0-9]*\"/version = \"$VERSION\"/" pyproject.toml

echo "Updated version to $VERSION"

# Commit the version bump
git add pyproject.toml
git commit -m "Bump version to $VERSION"

# Create and push tag
git tag -a "v$VERSION" -m "Release version $VERSION"
git push origin main
git push origin "v$VERSION"

echo ""
echo "✅ Release v$VERSION triggered!"
echo "GitHub Actions will now:"
echo "  1. Build the package"
echo "  2. Publish to PyPI"
echo "  3. Create a GitHub release"
echo ""
echo "Monitor progress at: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:\/]//;s/\.git$//')/actions"
