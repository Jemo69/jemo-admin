#!/bin/bash
# Script to create a new release using jj (Jujutsu) and git

# Check if version argument is provided
if [ -z "$1" ]; then
    echo "Usage: ./release.sh <version>"
    echo "Example: ./release.sh 0.1.5"
    exit 1
fi

VERSION=$1

echo "🔄 Creating release v$VERSION"

# Update version in pyproject.toml
sed -i "s/version = \"[0-9]*\.[0-9]*\.[0-9]*\"/version = \"$VERSION\"/" pyproject.toml

echo "✅ Updated version to $VERSION"

# Stage the change with jj (jj tracks all changes automatically)
jj describe -m "Bump version to $VERSION"

echo "✅ Committed change with jj"

# Push the commit to main
jj bookmark set main -r @
jj git push

echo "✅ Pushed to main"

# Get the git directory
GIT_DIR=$(jj git root)
cd "$GIT_DIR"

# Create git tag using regular git (jj doesn't have a tag command)
git tag -a "v$VERSION" -m "Release version $VERSION"

echo "✅ Created tag v$VERSION"

# Push the tag to trigger GitHub Actions release workflow
git push origin "v$VERSION"

echo ""
echo "🚀 Release v$VERSION triggered!"
echo "GitHub Actions will now:"
echo "  1. Build the package"
echo "  2. Publish to PyPI"
echo "  3. Create a GitHub release"
echo ""

# Get repository info from git remote
REPO_URL=$(git remote get-url origin 2>/dev/null | sed 's/.*github.com[:/]//;s/.git$//')
if [ -n "$REPO_URL" ]; then
    echo "📊 Monitor progress at: https://github.com/$REPO_URL/actions"
else
    echo "📊 Check your GitHub repository Actions tab"
fi
