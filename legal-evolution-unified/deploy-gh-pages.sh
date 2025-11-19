#!/bin/bash

# Deploy to GitHub Pages Script
# Builds the app and deploys to gh-pages branch

set -e

echo "🚀 Deploying to GitHub Pages..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Run this script from the repository root."
    exit 1
fi

# Step 1: Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
npm install

# Step 2: Build the app
echo -e "${BLUE}🔨 Building application...${NC}"
BASE_PATH=/legal-evolution-unified npm run build

# Step 3: Add .nojekyll file (tells GitHub Pages not to use Jekyll)
echo -e "${BLUE}📝 Adding .nojekyll file...${NC}"
touch dist/.nojekyll

# Step 4: Add CNAME if custom domain is configured
# Uncomment and modify if you have a custom domain:
# echo "legal-evolution.yourdomain.com" > dist/CNAME

# Step 5: Deploy to gh-pages branch
echo -e "${BLUE}🚀 Deploying to gh-pages branch...${NC}"

# Check if gh-pages branch exists
if git show-ref --verify --quiet refs/heads/gh-pages; then
    echo "gh-pages branch exists, will update it"
else
    echo "Creating gh-pages branch"
    git branch gh-pages
fi

# Navigate to dist folder
cd dist

# Initialize git if needed
if [ ! -d ".git" ]; then
    git init
    git remote add origin $(git -C .. config --get remote.origin.url)
fi

# Commit and push
git add -A
git commit -m "Deploy to GitHub Pages - $(date)"
git push -f origin HEAD:gh-pages

cd ..

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "Your app will be available at:"
echo "https://adrianlerer.github.io/legal-evolution-unified/"
echo ""
echo "Note: First deployment may take 5-10 minutes to become available."
echo ""
echo "To check deployment status:"
echo "https://github.com/adrianlerer/legal-evolution-unified/deployments"
