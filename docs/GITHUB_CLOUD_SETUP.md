# GitHub Cloud Development Setup - vidianews

**Project**: vidianews_27092026 - AI Publishing Platform  
**Repository**: https://github.com/nollyvenon/vidianews_27092026  
**Status**: Ready for GitHub Cloud Development & CI/CD  
**Date**: 2026-09-27

---

## Overview

All 175 modules will be built entirely in GitHub Cloud using:
- ✅ **GitHub Codespaces** - Cloud-based development environment
- ✅ **GitHub Actions** - Automated CI/CD pipelines
- ✅ **GitHub Container Registry** - Docker image hosting
- ✅ **GitHub Cloud Infrastructure** - Automated testing and deployment

---

## 1. GitHub Codespaces (Cloud Development Environment)

### What is GitHub Codespaces?
A fully configured VS Code environment in the browser or desktop IDE, running in GitHub's cloud infrastructure.

### Quick Start

**Option A: Browser (Recommended for quick work)**
```bash
# Go to https://github.com/nollyvenon/vidianews_27092026
# Press '.' (period) key to open GitHub.dev editor
# OR click "Code" → "Codespaces" → "Create codespace on master"
```

**Option B: VS Code Desktop (Full IDE experience)**
```bash
# 1. Install GitHub Codespaces extension in VS Code
# 2. Open Command Palette (Ctrl+Shift+P)
# 3. Type "Codespaces: Create New Codespace"
# 4. Select master branch
# 5. Select machine type (4-core recommended for FastAPI + Next.js)
```

### Automatic Setup
When Codespaces starts:
1. ✅ Python 3.11 + pip installed
2. ✅ Node.js 20 + npm installed
3. ✅ FastAPI dependencies installed
4. ✅ Next.js dependencies installed
5. ✅ PostgreSQL 16 service running
6. ✅ Redis service running
7. ✅ All tests run and pass (if env configured)

### Running Services in Codespaces

**Backend (FastAPI)**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Auto-accessible at: https://{codespace-name}.github.dev:8000
```

**Frontend (Next.js)**
```bash
cd frontend
npm run dev
# Auto-accessible at: https://{codespace-name}.github.dev:3000
```

**Both in parallel** (use separate terminals in Codespaces)
```bash
# Terminal 1:
cd backend && uvicorn app.main:app --reload

# Terminal 2:
cd frontend && npm run dev
```

### Accessing Services
Codespaces automatically forwards ports:
- **Frontend**: http://localhost:3000 (or auto-forwarded HTTPS URL)
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

---

## 2. GitHub Actions CI/CD Pipelines

### Current Workflows

#### **ci-cd.yml** - Main Pipeline (Auto-runs on every push)
Runs on every commit to master/main/develop:
- ✅ **Backend Tests** - pytest with 90%+ coverage enforcement
- ✅ **Frontend Tests** - Jest + Playwright E2E tests
- ✅ **Mobile Tests** - Flutter widget/integration tests
- ✅ **Security Checks** - Bandit + Dependency scanning
- ✅ **Build Containers** - Docker images to GitHub Container Registry
- ✅ **Deploy** - Auto-deploy to production on master branch

#### **module-build.yml** - Module Builder (Manual trigger)
Build individual modules on-demand:
```bash
# Go to Actions tab → Module Builder → Run workflow
# Input:
#   Module number: 4
#   Module name: Multi-tenancy
```

### View CI/CD Status
```bash
# In GitHub:
1. Go to Actions tab
2. See all workflow runs
3. Click a run to see detailed logs
4. Check coverage reports and test results
```

### Local CI/CD Testing
Test the workflow locally before pushing:
```bash
# Install act (runs GitHub Actions locally)
# macOS:
brew install act

# Linux/Windows: See https://github.com/nektos/act

# Run workflow locally
act -j test-backend
act -j test-frontend
act -j quality-gate
```

---

## 3. GitHub Container Registry (Image Hosting)

### What Gets Built
Every push to master builds and pushes:
- `ghcr.io/nollyvenon/vidianews_27092026-backend:latest`
- `ghcr.io/nollyvenon/vidianews_27092026-frontend:latest`

### Pull Images for Local Development
```bash
# Login to GitHub Container Registry
docker login ghcr.io -u nollyvenon -p ${{ secrets.GITHUB_TOKEN }}

# Pull latest images
docker pull ghcr.io/nollyvenon/vidianews_27092026-backend:latest
docker pull ghcr.io/nollyvenon/vidianews_27092026-frontend:latest

# Run containers
docker run -p 8000:8000 ghcr.io/nollyvenon/vidianews_27092026-backend:latest
docker run -p 3000:3000 ghcr.io/nollyvenon/vidianews_27092026-frontend:latest
```

---

## 4. Development Workflow for 175 Modules

### Step 1: Create Codespace
```bash
# GitHub.com → Code → Codespaces → Create on master
# Wait ~5 minutes for full setup
```

### Step 2: Create Module Branch
```bash
git checkout -b module/4-multi-tenancy
```

### Step 3: Implement Module
```bash
# Backend service
vim backend/app/services/tenant_service.py

# API endpoints
vim backend/app/api/v1/tenants.py

# Frontend pages
touch frontend/app/dashboard/tenants/page.tsx

# Tests
touch backend/tests/unit/test_tenant_service.py
```

### Step 4: Test Locally in Codespaces
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Tests
cd backend
pytest tests/ -v --cov=app

# Ensure 90%+ coverage
coverage report --fail-under=90
```

### Step 5: Commit & Push
```bash
git add backend/app/services/tenant_service.py \
           backend/app/api/v1/tenants.py \
           frontend/app/dashboard/tenants/page.tsx \
           backend/tests/unit/test_tenant_service.py

git commit -m "Module 4: Multi-tenancy - Complete implementation with 90%+ test coverage"

git push origin module/4-multi-tenancy
```

### Step 6: CI/CD Runs Automatically
GitHub Actions **automatically**:
- Runs all tests
- Enforces 90%+ coverage
- Lints code
- Builds containers
- Posts results as PR comment

### Step 7: Create PR & Merge
```bash
# GitHub.com → Pull Requests → New PR
# GitHub Actions checks MUST pass before merge
# Once all ✅, merge to master
# Automatic deployment to production
```

---

## 5. Setting Up GitHub Secrets (One-time setup)

### Required Secrets for Deployment
```bash
# GitHub.com → Settings → Secrets and variables → Actions

# Add these secrets:
DEPLOY_KEY        # SSH private key for deployment server
DEPLOY_HOST        # Deployment server hostname
DEPLOY_USER        # SSH username
CODECOV_TOKEN      # For coverage reports (optional)
```

**To generate SSH key:**
```bash
ssh-keygen -t rsa -b 4096 -f deploy_key
# Copy private key to DEPLOY_KEY secret
# Add public key to deployment server ~/.ssh/authorized_keys
```

---

## 6. Monitoring Builds & Tests

### Real-time Monitoring
```bash
# GitHub.com → Actions tab → Watch workflows run live
```

### Coverage Reports
```bash
# After CI/CD completes:
# GitHub.com → Code Coverage tab (if Codecov integrated)
# OR check workflow logs for coverage percentage
```

### Test Results
```bash
# GitHub.com → Actions → Workflow run → Test Results
# Shows exactly which tests passed/failed
```

---

## 7. Module-by-Module Workflow (175 modules)

### For Each Module (110 minutes):
```bash
# 1. Start Codespace
codespace create

# 2. Create branch
git checkout -b module/X-name

# 3. Implement (following template)
# backend/app/models/
# backend/app/services/
# backend/app/api/v1/
# frontend/app/dashboard/
# mobile/lib/screens/
# tests/

# 4. Test locally (must pass)
pytest tests/ --cov=app --cov-report=term-missing
npm run test:unit

# 5. Commit
git commit -m "Module X: Name - Full implementation with 90%+ coverage"

# 6. Push & CI/CD auto-tests
git push

# 7. Merge PR
gh pr create --fill
gh pr merge --auto
```

### Expected Time per Module
- **Development**: 60 minutes (local Codespaces)
- **CI/CD Pipeline**: 15 minutes (automated tests, builds, deploy)
- **Total**: 75-110 minutes per module
- **For 175 modules**: ~250 hours total (manageable in parallel across team)

---

## 8. Troubleshooting

### Codespaces Won't Start
```bash
# 1. Check if service quota exceeded
# 2. Create new codespace (old one may be stuck)
# 3. Use VS Code desktop instead if browser fails
```

### Tests Fail in CI/CD but Pass Locally
```bash
# CI/CD uses different environment:
# - Ubuntu Linux (not Windows)
# - Isolated database
# - Read-only file system restrictions

# Test with act locally:
act -j test-backend --secret GITHUB_TOKEN=$(gh auth token)
```

### Docker Images Won't Push
```bash
# Check GitHub token permissions:
# Settings → Personal access tokens → Ensure 'packages:write' scope
```

### Deployment Fails
```bash
# Check DEPLOY_* secrets are set:
# GitHub → Settings → Secrets → Verify all exist

# Test SSH manually:
ssh -i ~/.ssh/deploy_key user@deploy_host
```

---

## 9. Key Commands Reference

### Codespaces
```bash
# Create codespace
gh codespace create -r nollyvenon/vidianews_27092026 -b master

# List codespaces
gh codespace list

# Connect to codespace
gh codespace code -c <codespace-name>

# Delete codespace
gh codespace delete -c <codespace-name>
```

### GitHub CLI
```bash
# Login
gh auth login

# Create PR
gh pr create --title "Module X: Name" --body "Full description"

# Check PR status
gh pr status

# Merge PR
gh pr merge --auto

# View Actions
gh run list
gh run view <run-id>
```

### Local Testing
```bash
# Test workflow locally with act
act -j test-backend
act -j test-frontend
act -l  # List all jobs

# Watch build logs
gh run watch <run-id>
```

---

## 10. Best Practices

### ✅ DO:
- Create Codespace for each module branch
- Run tests locally before pushing
- Use `git push origin module/X-name` for all module work
- Commit with meaningful messages
- Let CI/CD run fully before merging
- Monitor Actions tab for any failures

### ❌ DON'T:
- Force push to master
- Skip local tests
- Ignore CI/CD failures
- Deploy without all checks passing
- Commit without branch protection
- Work directly on master

---

## Summary

**vidianews is now fully set up for GitHub Cloud development:**

| Component | Tool | Status |
|-----------|------|--------|
| 💻 Cloud IDE | GitHub Codespaces | ✅ Ready |
| 🔄 CI/CD | GitHub Actions | ✅ Ready (2 workflows) |
| 📦 Containers | GitHub Container Registry | ✅ Ready |
| 🚀 Deployment | GitHub Actions → Cloud | ✅ Configured |
| 📊 Coverage | Codecov integration | ✅ Enforced (90%+) |
| 🧪 Testing | pytest + Jest + Flutter | ✅ Automated |

**To start building modules:**

1. Open GitHub.com → Code → Codespaces
2. Create codespace on master
3. Branch: `git checkout -b module/X-name`
4. Code → Test → Commit → Push
5. GitHub Actions auto-deploys ✅

---

**Status**: All systems ready for 175-module build-out in GitHub Cloud 🚀

For questions: Check Actions logs → Codespaces docs → GitHub CLI help
