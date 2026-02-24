# ZipCode Population Density API - Deployment Guide

## 🚀 Quick Deployment to Azure Windows VM

This guide provides step-by-step instructions for deploying the ZipCode Population Density API container to an Azure Windows VM.

## 📋 Prerequisites

### Azure Windows VM Requirements
- Windows Server 2019 or later
- Docker Desktop for Windows installed
- At least 2GB RAM available for the container
- Ports 80 and 8000 open in the firewall
- Internet connection for pulling the container image

### Container Image
The API is available as a container image at:
```
ghcr.io/rypatch/zipcode-api:latest
```

## 🔧 Installation Methods

### Method 1: Automated PowerShell Deployment (Recommended)

1. **Download the deployment script** to your Windows VM:
   ```powershell
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/rypatch/ZipAPI/main/deploy-windows.ps1" -OutFile "deploy-zipcode-api.ps1"
   ```

2. **Run the deployment script** (as Administrator):
   ```powershell
   PowerShell -ExecutionPolicy Bypass -File "deploy-zipcode-api.ps1"
   ```

3. **Access the API**:
   - API Documentation: `http://localhost/docs`
   - Health Check: `http://localhost/health`
   - Direct API Access: `http://localhost:8000/docs`

### Method 2: Manual Docker Commands

1. **Pull the container image**:
   ```powershell
   docker pull ghcr.io/rypatch/zipcode-api:latest
   ```

2. **Run the container**:
   ```powershell
   docker run -d `
     --name zipcode-api-prod `
     --restart unless-stopped `
     -p 80:8000 `
     -p 8000:8000 `
     -e PYTHONUNBUFFERED=1 `
     -e LOG_LEVEL=INFO `
     --health-cmd="curl -f http://localhost:8000/health || exit 1" `
     --health-interval=30s `
     --health-timeout=10s `
     --health-retries=3 `
     --health-start-period=60s `
     ghcr.io/rypatch/zipcode-api:latest
   ```

3. **Verify the deployment**:
   ```powershell
   docker ps
   docker logs zipcode-api-prod
   ```

### Method 3: Docker Compose (Advanced)

1. **Download the production compose file**:
   ```powershell
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/rypatch/ZipAPI/main/docker-compose.prod.yml" -OutFile "docker-compose.prod.yml"
   ```

2. **Edit the compose file** to replace `rypatch` with your GitHub username:
   ```yaml
   image: ghcr.io/YOUR_USERNAME/zipcode-api:latest
   ```

3. **Deploy with Docker Compose**:
   ```powershell
   docker-compose -f docker-compose.prod.yml up -d
   ```

## 🔄 Automatic Startup Configuration

### Option 1: Docker Restart Policy (Recommended)
The container is configured with `--restart unless-stopped`, which means:
- ✅ Starts automatically when Docker starts
- ✅ Restarts if the container crashes
- ✅ Won't restart if manually stopped

### Option 2: Windows Service (Advanced)
To ensure Docker starts with Windows and the container runs at boot:

1. **Configure Docker Desktop** to start at login
2. **Create a Windows Task** to run the deployment script at startup:
   ```powershell
   $action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File C:\path\to\deploy-zipcode-api.ps1"
   $trigger = New-ScheduledTaskTrigger -AtStartup
   $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
   Register-ScheduledTask -TaskName "ZipCode API Startup" -Action $action -Trigger $trigger -Settings $settings -User "SYSTEM"
   ```

## 🌐 Accessing the API

### API Endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check - returns API status |
| `GET /docs` | Interactive API documentation (Swagger UI) |
| `GET /openapi.json` | OpenAPI schema |
| `POST /api/v1/zipcode/density` | Assess zipcode population density |
| `GET /api/v1/zipcode/{zipcode}/nearby` | Get nearby zipcodes |
| `GET /api/v1/zipcode/{zipcode}/stats` | Get zipcode statistics |

### Example API Usage

**Health Check:**
```powershell
Invoke-RestMethod -Uri "http://localhost/health"
```

**Assess Zipcode Density:**
```powershell
$body = @{ zipcode = "10001"; radius_miles = 25.0 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost/api/v1/zipcode/density" -Method POST -Body $body -ContentType "application/json"
```

## 🔍 Monitoring and Troubleshooting

### Container Management Commands

**Check container status:**
```powershell
docker ps -a --filter name=zipcode-api-prod
```

**View container logs:**
```powershell
docker logs zipcode-api-prod
# Follow logs in real-time
docker logs -f zipcode-api-prod
```

**Restart the container:**
```powershell
docker restart zipcode-api-prod
```

**Update to latest version:**
```powershell
docker pull ghcr.io/rypatch/zipcode-api:latest
docker stop zipcode-api-prod
docker rm zipcode-api-prod
# Re-run the deployment script or docker run command
```

### Health Monitoring

The container includes built-in health checks:
```powershell
# Check health status
docker inspect --format="{{.State.Health.Status}}" zipcode-api-prod

# Get detailed health info
docker inspect --format="{{json .State.Health}}" zipcode-api-prod | ConvertFrom-Json
```

### Performance Monitoring

**Container resource usage:**
```powershell
docker stats zipcode-api-prod
```

**API performance test:**
```powershell
# Simple performance test
Measure-Command { 
    Invoke-RestMethod -Uri "http://localhost/health" 
}
```

## 🔧 Configuration Options

### Environment Variables
You can customize the container behavior with environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `PYTHONUNBUFFERED` | `1` | Ensure Python output is sent straight to terminal |
| `PORT` | `8000` | Internal container port (don't change) |

**Example with custom logging:**
```powershell
docker run -d `
  --name zipcode-api-prod `
  --restart unless-stopped `
  -p 80:8000 `
  -e LOG_LEVEL=DEBUG `
  ghcr.io/rypatch/zipcode-api:latest
```

## 🛡️ Security Considerations

### Firewall Configuration
Ensure these ports are configured in Windows Firewall:
- **Port 80**: HTTP traffic to the API
- **Port 8000**: Direct API access (optional, can be closed)

### Network Security
- The container runs as a non-root user for security
- Consider using HTTPS in production with a reverse proxy
- Limit access to management ports (Docker API, etc.)

### Updates
- Regularly update the container image to get security patches
- Monitor the GitHub repository for security advisories
- Use specific version tags instead of `latest` in production

## 📊 Container Resources

### Default Resource Limits
- **Memory**: 512MB limit, 256MB reserved
- **CPU**: Shared CPU access (no hard limits)
- **Network**: Bridge network with health checks

### Scaling Considerations
For high-traffic deployments:
- Use multiple container instances with a load balancer
- Consider Azure Container Instances or Azure Kubernetes Service
- Monitor memory usage and scale accordingly

## 🆘 Support and Troubleshooting

### Common Issues

**Container won't start:**
1. Check Docker is running: `docker version`
2. Check port availability: `netstat -an | findstr :80`
3. Check container logs: `docker logs zipcode-api-prod`

**Health check failing:**
1. Wait 60 seconds for startup period
2. Check if port 8000 is accessible inside container
3. Verify the health endpoint manually: `curl http://localhost:8000/health`

**API returning 500 errors:**
1. Check container logs for Python errors
2. Verify the zipcode data loaded correctly
3. Test with a simple health check first

### Getting Help
- **GitHub Issues**: [Create an issue](https://github.com/rypatch/ZipAPI/issues) for bugs or feature requests
- **API Documentation**: Access `/docs` endpoint for interactive API documentation
- **Container Logs**: Always include relevant log output when requesting help

---

## 🎉 Deployment Complete!

Your ZipCode Population Density API should now be running and accessible at:
- **API Documentation**: http://your-vm-ip/docs
- **Health Check**: http://your-vm-ip/health

The container will automatically restart if the VM reboots, ensuring high availability of your API service.