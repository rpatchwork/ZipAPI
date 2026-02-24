#!/usr/bin/env pwsh
<#
.SYNOPSIS
    GitHub Publishing Script for ZipCode API
.DESCRIPTION
    Automates the process of publishing the ZipCode Population Density API to GitHub
    with automated container builds and deployment configuration.
.PARAMETER CommitMessage
    Custom commit message (optional)
.PARAMETER SkipBuildWait
    Don't wait for GitHub Actions build to complete
.PARAMETER TestDeployment
    Run local deployment test after publishing
.EXAMPLE
    .\publish-github.ps1
    .\publish-github.ps1 -CommitMessage "Feature: Added new density calculation algorithm"
    .\publish-github.ps1 -SkipBuildWait -TestDeployment
#>

param(
    [string]$CommitMessage = "Production deployment: containerized FastAPI with Azure Windows VM support",
    [switch]$SkipBuildWait,
    [switch]$TestDeployment
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Color functions
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "📋 $Message" -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }

Write-Host "========================================" -ForegroundColor Blue
Write-Host "   ZipCode API - GitHub Publishing      " -ForegroundColor Blue  
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

try {
    # Verify we're in the correct directory
    Write-Info "[1/8] Verifying project directory..."
    if (-not (Test-Path "app\main.py")) {
        throw "Please run this script from the ZipAPI root directory. Expected to find: app\main.py"
    }
    Write-Success "Project structure verified"

    # Check Git repository status
    Write-Info "[2/8] Checking Git repository status..."
    try {
        $gitStatus = git status --porcelain 2>$null
        $gitRemote = git remote get-url origin 2>$null
    } catch {
        throw "Not a Git repository. Please initialize first:`n  git init`n  git remote add origin https://github.com/YOUR_USERNAME/ZipAPI.git"
    }

    if (-not $gitRemote) {
        throw "No Git remote found. Please add remote:`n  git remote add origin https://github.com/YOUR_USERNAME/ZipAPI.git"
    }

    Write-Success "Git repository configured: $gitRemote"

    # Update container image references
    Write-Info "[3/8] Updating container image references..."
    $username = ($gitRemote -split '/')[3]  # Extract username from GitHub URL
    
    if ($username -eq "YOUR_USERNAME") {
        Write-Warning "Please update YOUR_USERNAME in the GitHub URL to your actual username"
        $username = Read-Host "Enter your GitHub username"
    }

    # Update files with actual username
    $filesToUpdate = @(
        @{Path = "docker-compose.prod.yml"; Pattern = "ghcr\.io/[^/]+/"; Replacement = "ghcr.io/$username/"},
        @{Path = "deploy-windows.ps1"; Pattern = 'ghcr\.io/[^/]+/'; Replacement = "ghcr.io/$username/"},
        @{Path = "deploy-windows.bat"; Pattern = 'ghcr\.io/[^/]+/'; Replacement = "ghcr.io/$username/"},
        @{Path = "DEPLOYMENT.md"; Pattern = 'ghcr\.io/[^/]+/'; Replacement = "ghcr.io/$username/"},
        @{Path = "GITHUB_SETUP.md"; Pattern = 'YOUR_USERNAME'; Replacement = $username},
        @{Path = "README.md"; Pattern = 'ghcr\.io/[^/]+/'; Replacement = "ghcr.io/$username/"}
    )

    foreach ($file in $filesToUpdate) {
        if (Test-Path $file.Path) {
            (Get-Content $file.Path) -replace $file.Pattern, $file.Replacement | Set-Content $file.Path
        }
    }
    Write-Success "Container references updated for user: $username"

    # Add files to Git
    Write-Info "[4/8] Adding files to Git..."
    git add .
    Write-Success "Files staged for commit"

    # Create commit
    Write-Info "[5/8] Creating commit..."
    git commit -m $CommitMessage
    Write-Success "Commit created: $CommitMessage"

    # Push to GitHub
    Write-Info "[6/8] Pushing to GitHub..."
    git push origin main
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to push to GitHub. Please check repository permissions and authentication."
    }
    Write-Success "Successfully pushed to GitHub!"

    # Get repository URL for actions
    $repoUrl = $gitRemote -replace '\.git$', ''
    $actionsUrl = "$repoUrl/actions"

    Write-Info "[7/8] Monitoring GitHub Actions build..."
    Write-Host ""
    Write-Success "Files pushed to GitHub successfully!"
    Write-Host ""
    Write-Host "🔗 Repository: $repoUrl" -ForegroundColor Blue
    Write-Host "⚙️  Actions: $actionsUrl" -ForegroundColor Blue  
    Write-Host "📦 Container: ghcr.io/$username/zipcode-api:latest" -ForegroundColor Blue
    Write-Host ""

    if (-not $SkipBuildWait) {
        Write-Info "Waiting for GitHub Actions build to start..."
        Write-Host "   (This may take 30-60 seconds for GitHub to pick up the push)" -ForegroundColor Gray
        
        # Wait for build to potentially start
        Start-Sleep -Seconds 30
        
        Write-Info "Build should now be running. Check the Actions tab for progress."
        Write-Host "   Expected build time: 3-5 minutes" -ForegroundColor Gray
        
        $openActions = Read-Host "Open GitHub Actions in browser? (y/n)"
        if ($openActions -eq 'y') {
            Start-Process $actionsUrl
        }
    }

    # Test deployment
    Write-Info "[8/8] Deployment testing..."
    if ($TestDeployment) {
        Write-Info "Running local deployment test..."
        & ".\deploy-windows.ps1" -SkipStartupConfig -TestMode
    } else {
        $testLocal = Read-Host "Test deployment locally? (y/n)"
        if ($testLocal -eq 'y') {
            Write-Info "Running local deployment test..."
            & ".\deploy-windows.ps1" -SkipStartupConfig -TestMode  
        }
    }

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   ✅ Publishing Complete!              " -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Success "Your ZipCode API is now:"
    Write-Host "  • Published to GitHub with full source code" -ForegroundColor White
    Write-Host "  • Building automatically with GitHub Actions" -ForegroundColor White  
    Write-Host "  • Ready for Azure VM deployment" -ForegroundColor White
    Write-Host "  • Available as a container image" -ForegroundColor White
    Write-Host ""
    Write-Info "📖 Next steps:"
    Write-Host "  • Monitor build: $actionsUrl" -ForegroundColor Gray
    Write-Host "  • Deploy to Azure VM: See DEPLOYMENT.md" -ForegroundColor Gray
    Write-Host "  • Configure GitHub: See GITHUB_SETUP.md" -ForegroundColor Gray
    Write-Host ""

} catch {
    Write-Host ""
    Write-Error "Publishing failed: $($_.Exception.Message)"
    Write-Host ""
    Write-Warning "Troubleshooting steps:"
    Write-Host "  1. Ensure you're in the ZipAPI root directory" -ForegroundColor Gray
    Write-Host "  2. Verify Git remote is configured correctly" -ForegroundColor Gray
    Write-Host "  3. Check GitHub authentication (git config --list)" -ForegroundColor Gray
    Write-Host "  4. Ensure repository exists on GitHub" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Manual commands:" -ForegroundColor Yellow
    Write-Host "  git remote -v" -ForegroundColor Gray
    Write-Host "  git status" -ForegroundColor Gray  
    Write-Host "  git push origin main" -ForegroundColor Gray
    Write-Host ""
    exit 1
}