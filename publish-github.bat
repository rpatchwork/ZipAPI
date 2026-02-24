@echo off
REM Quick GitHub Publishing Script for ZipCode API
echo ========================================
echo   ZipCode API - GitHub Publishing
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo ERROR: Please run this script from the ZipAPI root directory
    echo Expected to find: app\main.py
    pause
    exit /b 1
)

echo [1/6] Checking Git status...
git status --porcelain > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Not a Git repository. Please initialize first:
    echo   git init
    echo   git remote add origin https://github.com/YOUR_USERNAME/ZipAPI.git
    pause
    exit /b 1
)

echo [2/6] Adding all files to Git...
git add .

echo [3/6] Creating commit...
set /p commit_message="Enter commit message (or press Enter for default): "
if "%commit_message%"=="" (
    set commit_message=Production deployment: containerized FastAPI with Azure Windows VM support
)
git commit -m "%commit_message%"

echo [4/6] Pushing to GitHub...
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to push to GitHub. Please check:
    echo 1. Remote repository exists: https://github.com/YOUR_USERNAME/ZipAPI
    echo 2. You have push permissions
    echo 3. Git is authenticated
    echo.
    echo You can push manually with: git push origin main
    pause
    exit /b 1
)

echo [5/6] Checking GitHub Actions...
echo.
echo ✅ Files pushed to GitHub successfully!
echo.
echo Next steps:
echo 1. Go to: https://github.com/YOUR_USERNAME/ZipAPI/actions
echo 2. Monitor the "Build and Deploy ZipCode API" workflow
echo 3. Build should complete in 3-5 minutes
echo 4. Container image will be available at: ghcr.io/YOUR_USERNAME/zipcode-api:latest
echo.

echo [6/6] Testing local deployment...
echo Would you like to test the deployment script locally? (y/n)
set /p test_local=
if /i "%test_local%"=="y" (
    echo.
    echo Running local deployment test...
    powershell.exe -ExecutionPolicy Bypass -File "deploy-windows.ps1" -SkipStartupConfig -TestMode
)

echo.
echo ========================================
echo   ✅ Publishing Complete!
echo ========================================
echo.
echo Your ZipCode API is now:
echo • Published to GitHub with full source code
echo • Building automatically with GitHub Actions
echo • Ready for Azure VM deployment
echo • Available as a container image
echo.
echo 📖 Next: See DEPLOYMENT.md for Azure VM setup
echo 🐙 Setup: See GITHUB_SETUP.md for configuration
echo.
pause