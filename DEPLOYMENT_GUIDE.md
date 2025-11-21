# 🚢 Deployment Guide - Legal Evolution Research Suite

**Version**: 1.0.0  
**Last Updated**: 2025-11-21

This guide covers deployment options for the Legal Evolution Research Suite, including GitHub Pages, Vercel, Railway, and self-hosted solutions.

---

## 📋 Table of Contents

1. [GitHub Pages (Static UI)](#github-pages-static-ui)
2. [Streamlit Cloud (Easiest)](#streamlit-cloud-easiest)
3. [Vercel (Frontend + Backend)](#vercel-frontend--backend)
4. [Railway (Backend API)](#railway-backend-api)
5. [Self-Hosted (Docker)](#self-hosted-docker)
6. [Environment Configuration](#environment-configuration)

---

## 1. GitHub Pages (Static UI)

Deploy Streamlit UI as static site to GitHub Pages.

### Prerequisites

- GitHub repository
- GitHub Actions enabled
- GitHub Pages enabled in repository settings

### Step 1: Create GitHub Pages Workflow

Create `.github/workflows/deploy-pages.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Build Streamlit to Static
        run: |
          # Convert Streamlit app to static HTML
          # Note: Streamlit doesn't natively support static builds
          # Use stlite (Streamlit + WebAssembly) for static deployment
          pip install stlite
          stlite pack frontend/streamlit/app.py build/
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './build'
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Step 2: Enable GitHub Pages

1. Go to repository **Settings > Pages**
2. **Source**: GitHub Actions
3. Save

### Step 3: Push to Deploy

```bash
git add .github/workflows/deploy-pages.yml
git commit -m "Add GitHub Pages deployment"
git push origin main
```

**Access**: `https://your-username.github.io/legal-evolution-unified/`

### ⚠️ Limitations

- Static UI only (no backend API)
- Limited interactivity (no real-time calculations unless using stlite)
- Best for documentation and static visualizations

---

## 2. Streamlit Cloud (Easiest)

**Recommended for quick deployment**

### Prerequisites

- Streamlit Cloud account (free): https://streamlit.io/cloud
- GitHub repository

### Step 1: Connect Repository

1. Go to https://share.streamlit.io/
2. Click **New app**
3. Connect GitHub repository
4. Select:
   - **Repository**: `your-username/legal-evolution-unified`
   - **Branch**: `main`
   - **Main file path**: `frontend/streamlit/app.py`

### Step 2: Configure Settings

- **Python version**: 3.11
- **Requirements file**: `requirements.txt`

### Step 3: Deploy

Click **Deploy!**

**Access**: `https://your-app-name.streamlit.app`

### ✅ Advantages

- ✅ Zero configuration
- ✅ Free tier available
- ✅ Automatic redeployment on git push
- ✅ HTTPS included
- ✅ Custom domains supported

### ⚠️ Limitations

- Backend API requires separate deployment (use Railway/Vercel)
- Free tier has resource limits (1GB RAM, shared CPU)

---

## 3. Vercel (Frontend + Backend)

Deploy both Streamlit UI and FastAPI backend.

### Prerequisites

- Vercel account (free): https://vercel.com/
- Vercel CLI: `npm install -g vercel`

### Step 1: Create `vercel.json`

Create `vercel.json` in repository root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    },
    {
      "src": "frontend/streamlit/app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/app.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/streamlit/app.py"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.11"
  }
}
```

### Step 2: Deploy

```bash
# Login to Vercel
vercel login

# Deploy
vercel --prod
```

**Access**: `https://your-app.vercel.app`

### ✅ Advantages

- ✅ Serverless architecture (scales automatically)
- ✅ Free tier generous (100GB bandwidth/month)
- ✅ Custom domains
- ✅ Automatic HTTPS
- ✅ Global CDN

---

## 4. Railway (Backend API)

Deploy FastAPI backend to Railway.

### Prerequisites

- Railway account (free): https://railway.app/
- Railway CLI: `npm install -g @railway/cli`

### Step 1: Create `railway.json`

Create `railway.json`:

```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r backend/requirements.txt"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Deploy

```bash
# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

**Access**: `https://your-app.railway.app`

### Step 3: Environment Variables

Set in Railway dashboard:
- `BACKEND_URL`: Your Railway app URL
- `ALLOWED_ORIGINS`: Frontend URL for CORS

### ✅ Advantages

- ✅ Free tier ($5/month credit)
- ✅ Automatic SSL
- ✅ Easy database integration (PostgreSQL, Redis)
- ✅ Monitoring included

---

## 5. Self-Hosted (Docker)

Deploy on your own server using Docker.

### Step 1: Create `Dockerfile`

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose ports
EXPOSE 8000 8501

# Start services
CMD ["sh", "-c", "uvicorn backend.app:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlit/app.py --server.port 8501 --server.address 0.0.0.0"]
```

### Step 2: Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - BACKEND_URL=http://localhost:8000
    volumes:
      - ./data:/app/data
      - ./reports:/app/reports
    restart: unless-stopped
  
  frontend:
    build: .
    command: streamlit run frontend/streamlit/app.py --server.port 8501 --server.address 0.0.0.0
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped
```

### Step 3: Create `nginx.conf`

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }
    
    upstream frontend {
        server frontend:8501;
    }
    
    server {
        listen 80;
        server_name your-domain.com;
        
        location /api/ {
            proxy_pass http://backend/api/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
        
        location / {
            proxy_pass http://frontend/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```

### Step 4: Deploy

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

**Access**: `http://your-server-ip` or `https://your-domain.com`

### ✅ Advantages

- ✅ Full control over infrastructure
- ✅ No vendor lock-in
- ✅ Suitable for production workloads
- ✅ Can run on-premises

---

## 6. Environment Configuration

### Required Environment Variables

Create `.env` file:

```env
# Backend API
BACKEND_URL=http://localhost:8000
ALLOWED_ORIGINS=http://localhost:8501,https://your-domain.com

# Feature Flags
ENABLE_ALL_FEATURES=true
REQUIRE_AUTH=false

# SaaS Configuration (optional)
SAAS_MODE=false
STRIPE_API_KEY=sk_test_...
POSTGRES_URL=postgresql://user:pass@localhost:5432/legal_evolution

# Logging
LOG_LEVEL=INFO
```

### Feature Configuration

Create `config/features.json`:

```json
{
  "cli_calculator": {"enabled": true},
  "cli_cultural_calculator": {"enabled": true},
  "dual_index_analyzer": {"enabled": true},
  "rootfinder": {"enabled": true},
  "paper_builder": {"enabled": true},
  "cli_matrix_visualizer": {"enabled": true},
  "genspark_assistant": {"enabled": true},
  "code_reviewer": {"enabled": false},
  "root_cause_analyzer": {"enabled": false},
  "ept_analyzer": {"enabled": false},
  "paleontology_tool": {"enabled": false},
  "golden_ratio_detector": {"enabled": false}
}
```

---

## 🔒 Security Considerations

### Production Checklist

- [ ] Enable HTTPS (use Let's Encrypt for free SSL)
- [ ] Set secure `ALLOWED_ORIGINS` (no wildcards in production)
- [ ] Use environment variables for secrets (never commit to git)
- [ ] Enable authentication if deploying publicly
- [ ] Set up rate limiting (prevent abuse)
- [ ] Configure CORS properly
- [ ] Use secure headers (Helmet.js equivalent)
- [ ] Enable logging and monitoring
- [ ] Set up automated backups
- [ ] Configure firewall rules

---

## 📊 Monitoring

### Recommended Tools

- **Uptime monitoring**: UptimeRobot (free)
- **Error tracking**: Sentry (free tier)
- **Analytics**: Plausible (privacy-friendly)
- **Logs**: Papertrail or Logtail

---

## 🚀 Deployment Comparison

| Option | Ease | Cost | Scalability | Control | Best For |
|--------|------|------|-------------|---------|----------|
| **GitHub Pages** | ⭐⭐⭐⭐⭐ | Free | Low | Low | Static docs |
| **Streamlit Cloud** | ⭐⭐⭐⭐⭐ | Free-$200/mo | Medium | Low | Demos, prototypes |
| **Vercel** | ⭐⭐⭐⭐ | Free-$20/mo | High | Medium | Production UI |
| **Railway** | ⭐⭐⭐⭐ | $5-$50/mo | High | Medium | Production API |
| **Docker (Self-hosted)** | ⭐⭐ | $5-$100/mo | Very High | Full | Enterprise |

---

## 🎯 Recommended Deployment Strategy

### Development
- **UI**: Local Streamlit (`streamlit run frontend/streamlit/app.py`)
- **API**: Local FastAPI (`uvicorn backend.app:app --reload`)

### Staging
- **UI**: Streamlit Cloud (free tier)
- **API**: Railway (free tier)

### Production
- **UI**: Vercel (Pro plan $20/mo)
- **API**: Railway (Hobby plan $5/mo) or self-hosted Docker
- **CDN**: Cloudflare (free)
- **Monitoring**: Sentry + UptimeRobot (free tiers)

---

## ❓ Troubleshooting

### Issue: Streamlit app not loading

**Solution**:
```bash
# Check if port 8501 is available
lsof -i :8501

# Kill process if needed
kill -9 <PID>

# Restart Streamlit
streamlit run frontend/streamlit/app.py
```

### Issue: Backend API CORS errors

**Solution**: Add frontend URL to `ALLOWED_ORIGINS` in `.env`:
```env
ALLOWED_ORIGINS=http://localhost:8501,https://your-frontend.vercel.app
```

### Issue: Docker build fails

**Solution**:
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

---

**Need help?** Open an issue: https://github.com/your-org/legal-evolution-unified/issues

**Last Updated**: 2025-11-21
