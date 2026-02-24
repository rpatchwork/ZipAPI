# ZipCode Population Density API - PowerShell Deployment Script
# This script sets up the container to run at Windows startup

param(
    [string]$ImageName = "ghcr.io/rypatch/zipcode-api:latest",
    [string]$ContainerName = "zipcode-api-prod",
    [int]$HttpPort = 80,
    [int]$ApiPort = 8000
)

Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "ZipCode Population Density API - Container Setup" -ForegroundColor Cyan  
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Pull latest image
Write-Host "Pulling latest ZipCode API container..." -ForegroundColor Yellow
try {
    docker pull $ImageName
    Write-Host "✓ Successfully pulled latest image" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Could not pull latest image. Using local image if available." -ForegroundColor Yellow
}

# Stop and remove existing container
Write-Host "Stopping any existing ZipCode API containers..." -ForegroundColor Yellow
docker stop $ContainerName 2>$null
docker rm $ContainerName 2>$null

# Start new container
Write-Host "Starting ZipCode API container in production mode..." -ForegroundColor Yellow

$dockerArgs = @(
    "run", "-d",
    "--name", $ContainerName,
    "--restart", "unless-stopped",
    "-p", "${HttpPort}:8000",
    "-p", "${ApiPort}:8000", 
    "-e", "PYTHONUNBUFFERED=1",
    "-e", "LOG_LEVEL=INFO",
    "--health-cmd", "curl -f http://localhost:8000/health || exit 1",
    "--health-interval", "30s",
    "--health-timeout", "10s", 
    "--health-retries", "3",
    "--health-start-period", "60s",
    $ImageName
)

try {
    $containerId = docker @dockerArgs
    Write-Host "✓ Container started successfully!" -ForegroundColor Green
    Write-Host "Container ID: $containerId" -ForegroundColor Gray
} catch {
    Write-Host "✗ Error: Failed to start container" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "API Endpoints:" -ForegroundColor Cyan
Write-Host "- Health Check: http://localhost:$HttpPort/health" -ForegroundColor White
Write-Host "- API Documentation: http://localhost:$HttpPort/docs" -ForegroundColor White
Write-Host "- Direct API Access: http://localhost:$ApiPort/docs" -ForegroundColor White
Write-Host ""

# Wait for container to be healthy
Write-Host "Waiting for API to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

$timeout = 60  # seconds
$elapsed = 0
$interval = 5

do {
    try {
        $health = docker inspect --format="{{.State.Health.Status}}" $ContainerName
        if ($health -eq "healthy") {
            Write-Host ""
            Write-Host "✓ ZipCode API is running and healthy!" -ForegroundColor Green
            Write-Host "✓ Access the API at: http://localhost:$HttpPort/docs" -ForegroundColor Green  
            Write-Host "✓ Container will restart automatically if the system reboots" -ForegroundColor Green
            break
        } elseif ($health -eq "starting") {
            Write-Host "Health check in progress..." -ForegroundColor Yellow
        } else {
            Write-Host "Health status: $health" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "Waiting for health check to initialize..." -ForegroundColor Yellow
    }
    
    Start-Sleep -Seconds $interval
    $elapsed += $interval
    
} while ($elapsed -lt $timeout)

if ($elapsed -ge $timeout) {
    Write-Host ""
    Write-Host "⚠ Warning: Health check timeout reached" -ForegroundColor Yellow
    Write-Host "Container may still be starting up. Check logs with:" -ForegroundColor Yellow
    Write-Host "docker logs $ContainerName" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Container Management Commands:" -ForegroundColor Cyan
Write-Host "- View logs: docker logs $ContainerName" -ForegroundColor Gray
Write-Host "- Stop container: docker stop $ContainerName" -ForegroundColor Gray  
Write-Host "- Start container: docker start $ContainerName" -ForegroundColor Gray
Write-Host "- Container status: docker ps -a --filter name=$ContainerName" -ForegroundColor Gray
Write-Host ""

Write-Host "Setup complete!" -ForegroundColor Green
Read-Host "Press Enter to exit"