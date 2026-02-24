# ZipCode Population Density API Container
# This Windows batch script sets up the container to run at Windows startup

@echo off
echo =================================================
echo ZipCode Population Density API - Container Setup
echo =================================================

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo Pulling latest ZipCode API container...
docker pull ghcr.io/rpatchwork/zipcode-api:latest

if errorlevel 1 (
    echo Warning: Could not pull latest image. Using local image if available.
)

echo Stopping any existing ZipCode API containers...
docker stop zipcode-api-prod 2>nul
docker rm zipcode-api-prod 2>nul

echo Starting ZipCode API container in production mode...
docker run -d ^
    --name zipcode-api-prod ^
    --restart unless-stopped ^
    -p 80:8000 ^
    -p 8000:8000 ^
    -e PYTHONUNBUFFERED=1 ^
    -e LOG_LEVEL=INFO ^
    --health-cmd="curl -f http://localhost:8000/health || exit 1" ^
    --health-interval=30s ^
    --health-timeout=10s ^
    --health-retries=3 ^
    --health-start-period=60s ^
    ghcr.io/rpatchwork/zipcode-api:latest

if errorlevel 1 (
    echo Error: Failed to start container
    pause
    exit /b 1
)

echo Container started successfully!
echo.
echo API Endpoints:
echo - Health Check: http://localhost/health
echo - API Documentation: http://localhost/docs
echo - Direct API Access: http://localhost:8000/docs
echo.
echo Waiting for API to be ready...
timeout /t 10 /nobreak >nul

REM Wait for health check
:waitloop
docker inspect --format="{{.State.Health.Status}}" zipcode-api-prod >nul 2>&1
if errorlevel 1 (
    echo Waiting for container health check...
    timeout /t 5 /nobreak >nul
    goto waitloop
)

for /f %%i in ('docker inspect --format="{{.State.Health.Status}}" zipcode-api-prod') do set HEALTH=%%i

if "%HEALTH%"=="healthy" (
    echo.
    echo ✓ ZipCode API is running and healthy!
    echo ✓ Access the API at: http://localhost/docs
    echo ✓ Container will restart automatically if the system reboots
) else (
    echo.
    echo Warning: Container started but health check is not yet healthy
    echo Status: %HEALTH%
    echo Check logs with: docker logs zipcode-api-prod
)

echo.
echo Setup complete! Press any key to exit...
pause >nul