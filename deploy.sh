#!/usr/bin/env bash
#
# deploy.sh — Initialize git repo, create GitHub repo, and push.
# Run this from inside the tuhow-blog/ directory.
#
set -euo pipefail

REPO_NAME="tuhow-blog"

echo "============================================"
echo "  Deploying ${REPO_NAME} to GitHub"
echo "============================================"

# 1. Initialize git repo
if [ ! -d ".git" ]; then
  echo "📦 Initializing git repository..."
  git init -b main
else
  echo "📦 Git repo already exists, skipping init."
fi

# 2. Add PaperMod theme as submodule (if not already added)
if [ ! -d "themes/PaperMod/.git" ] && [ ! -f "themes/PaperMod/.git" ]; then
  echo "🎨 Adding PaperMod theme as git submodule..."
  git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
else
  echo "🎨 PaperMod submodule already exists, skipping."
fi

# 3. Stage and commit
echo "📝 Staging all files..."
git add .
git commit -m "Initial commit: Hugo site migrated from WordPress" || echo "  (nothing to commit)"

# 4. Create GitHub repo
echo "🚀 Creating GitHub repository: ${REPO_NAME}..."
if gh repo view "${REPO_NAME}" &>/dev/null; then
  echo "  Repository already exists, skipping creation."
else
  gh repo create "${REPO_NAME}" --public --source=. --remote=origin --push
  echo "  ✅ Repository created and pushed!"
fi

# 5. Push if remote already existed
if git remote get-url origin &>/dev/null; then
  echo "⬆️  Pushing to origin/main..."
  git push -u origin main
fi

# 6. Enable GitHub Pages (deploy from Actions)
echo "⚙️  Configuring GitHub Pages to deploy from Actions..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/$(gh api user --jq .login)/${REPO_NAME}/pages" \
  -f "build_type=workflow" \
  2>/dev/null || \
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  "/repos/$(gh api user --jq .login)/${REPO_NAME}/pages" \
  -f "build_type=workflow" \
  -f "source[branch]=main" \
  -f "source[path]=/" \
  2>/dev/null || echo "  (Pages may need manual enable in repo Settings → Pages)"

echo ""
echo "============================================"
echo "  ✅ Done! Your site will be live at:"
echo "  https://$(gh api user --jq .login).github.io/${REPO_NAME}/"
echo ""
echo "  To use your custom domain (tuhow.tw):"
echo "  1. Go to repo Settings → Pages → Custom domain"
echo "  2. Enter: tuhow.tw"
echo "  3. Add a CNAME record pointing to"
echo "     $(gh api user --jq .login).github.io"
echo "============================================"
