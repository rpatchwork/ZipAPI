# GitHub Setup and Publishing Guide

This guide walks through publishing your ZipCode Population Density API to GitHub and setting up automated container builds.

## 📚 Table of Contents
1. [Initial GitHub Setup](#initial-github-setup)
2. [Repository Configuration](#repository-configuration)  
3. [Container Registry Setup](#container-registry-setup)
4. [Automated Builds](#automated-builds)
5. [Deployment Verification](#deployment-verification)

## 🚀 Initial GitHub Setup

### Step 1: Create GitHub Repository

1. **Go to GitHub** and click "New repository"
2. **Repository name**: `ZipAPI` (or your preferred name)
3. **Description**: "ZipCode Population Density Assessment API - Containerized FastAPI application for VM deployment"
4. **Visibility**: Public (required for GitHub Container Registry)
5. **Initialize**: ✅ Add a README file, ✅ Add .gitignore (Python), ✅ Add a license
6. **Click "Create repository"**

### Step 2: Clone and Setup Local Repository

```bash
# Clone the repository  
git clone https://github.com/YOUR_USERNAME/ZipAPI.git
cd ZipAPI

# Copy your project files to the repository
# (Copy all files from your C:\Users\rypatch\ZipAPI\ directory)

# Add files to git
git add .
git commit -m "Initial commit: ZipCode Population Density API"
git push origin main
```

## 🔧 Repository Configuration

### Update Image References

Before pushing, update the container image references in these files:

1. **docker-compose.prod.yml** - Line 6:
   ```yaml
   image: ghcr.io/YOUR_USERNAME/zipcode-api:latest
   ```

2. **deploy-windows.ps1** - Line 6:
   ```powershell
   [string]$ImageName = "ghcr.io/YOUR_USERNAME/zipcode-api:latest",
   ```

3. **deploy-windows.bat** - Line 14:
   ```batch
   docker pull ghcr.io/YOUR_USERNAME/zipcode-api:latest
   ```

4. **DEPLOYMENT.md** - Update all references from `rypatch` to `YOUR_USERNAME`

### Required Files Checklist

Ensure these files are in your repository:
- ✅ `Dockerfile` - Container build instructions
- ✅ `docker-compose.yml` - Development compose file
- ✅ `docker-compose.prod.yml` - Production compose file
- ✅ `.github/workflows/build-deploy.yml` - GitHub Actions workflow
- ✅ `.dockerignore` - Exclude unnecessary files from container
- ✅ `deploy-windows.ps1` - PowerShell deployment script
- ✅ `deploy-windows.bat` - Batch deployment script
- ✅ `DEPLOYMENT.md` - Complete deployment documentation
- ✅ `README.md` - Project documentation

## 📦 Container Registry Setup

### Enable GitHub Container Registry

1. **Go to your GitHub repository**
2. **Click on "Settings" tab**
3. **Scroll down to "Features" section**
4. **Check "Packages"** to enable GitHub Container Registry

### Configure Package Permissions

1. **Go to your profile → Packages**
2. **Find your `zipcode-api` package** (after first build)
3. **Click on the package → Settings**
4. **Set visibility to "Public"** (for easy deployment)
5. **Add repository access** if needed

## 🔄 Automated Builds

### GitHub Actions Workflow

The included `.github/workflows/build-deploy.yml` provides:

- ✅ **Automated builds** on push to main branch
- ✅ **Multi-architecture support** (AMD64, ARM64)
- ✅ **Automatic tagging** with version numbers
- ✅ **Container testing** before publishing
- ✅ **Python tests** to ensure code quality

### Trigger Your First Build

1. **Push your code** to the main branch:
   ```bash
   git add .
   git commit -m "Add containerization and deployment files"
   git push origin main
   ```

2. **Monitor the build** in GitHub:
   - Go to your repository → Actions tab
   - Watch the "Build and Deploy ZipCode API" workflow
   - Build should complete in 3-5 minutes

3. **Verify the container** was published:
   - Go to your repository main page
   - Look for "Packages" in the right sidebar
   - You should see `zipcode-api` package

## 🔍 Deployment Verification

### Test the Published Container

Once your container is built and published, test it locally:

```powershell
# Pull your published container
docker pull ghcr.io/YOUR_USERNAME/zipcode-api:latest

# Run a quick test
docker run --rm -d --name test-api -p 8000:8000 ghcr.io/YOUR_USERNAME/zipcode-api:latest

# Wait for startup
Start-Sleep -Seconds 30

# Test the health endpoint
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Stop the test container
docker stop test-api
```

Expected output:
```json
{
  "status": "healthy",
  "service": "zipcode-population-density-api", 
  "version": "1.0.0"
}
```

### Deploy to Azure VM

Once verified locally, use your deployment script on the Azure Windows VM:

```powershell
# Download and run deployment script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/YOUR_USERNAME/ZipAPI/main/deploy-windows.ps1" -OutFile "deploy.ps1"
PowerShell -ExecutionPolicy Bypass -File "deploy.ps1"
```

## 🏷️ Version Management

### Semantic Versioning

Use git tags to create versioned releases:

```bash
# Create a version tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

This will trigger a build with version-specific tags:
- `ghcr.io/YOUR_USERNAME/zipcode-api:v1.0.0`
- `ghcr.io/YOUR_USERNAME/zipcode-api:1.0`
- `ghcr.io/YOUR_USERNAME/zipcode-api:latest`

### Branch Strategy

**Recommended workflow:**
- `main` - Production-ready code, triggers latest builds
- `develop` - Development code, triggers development builds  
- `feature/*` - Feature branches, no automatic builds

## 🛠️ Advanced Configuration

### Custom Build Arguments

Modify `.github/workflows/build-deploy.yml` to add build arguments:

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    platforms: linux/amd64,linux/arm64
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    labels: ${{ steps.meta.outputs.labels }}
    build-args: |
      VERSION=${{ github.ref_name }}
      BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
```

### Private Container Registry

For private deployments, you can use:
1. **GitHub Container Registry** (private packages)
2. **Azure Container Registry** 
3. **Docker Hub** (private repositories)

## 🎯 Next Steps

1. **✅ Complete the GitHub setup** following this guide
2. **✅ Test the automated build** by pushing to main
3. **✅ Verify container deployment** on your Azure VM
4. **✅ Set up monitoring** and alerting for your API
5. **✅ Configure HTTPS** with a reverse proxy if needed
6. **✅ Set up backup** strategies for your zipcode data

## 📋 Troubleshooting

### Build Failures

**Common issues and solutions:**

1. **Docker build fails**:
   - Check Dockerfile syntax
   - Ensure all required files are included
   - Verify Python dependencies in requirements.txt

2. **Tests fail**:
   - Run tests locally first: `python -m pytest tests/ -v`
   - Check data loading in the test environment

3. **Container registry permissions**:
   - Ensure repository packages are enabled
   - Check GitHub token permissions
   - Verify package visibility settings

### Deployment Issues

1. **Cannot pull container**:
   - Verify the image name and tag
   - Check if the package is public
   - Ensure Docker is logged in: `docker login ghcr.io`

2. **Container startup fails**:
   - Check container logs: `docker logs container-name`
   - Verify port availability on the host
   - Ensure sufficient system resources

---

## 🎉 Success!

Your ZipCode Population Density API is now:
- ✅ **Published to GitHub** with full source code
- ✅ **Automatically built** with GitHub Actions  
- ✅ **Available as a container** for easy deployment
- ✅ **Ready for Azure VM** deployment
- ✅ **Documented** with comprehensive guides

**Repository URL**: https://github.com/YOUR_USERNAME/ZipAPI
**Container Image**: ghcr.io/YOUR_USERNAME/zipcode-api:latest