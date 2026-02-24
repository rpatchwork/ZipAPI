# ZipCode Population Density API - PowerShell Demo
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "ZipCode Population Density API Demo" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting API server..." -ForegroundColor Yellow
$serverJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\rypatch\ZipAPI"
    & "C:/Users/rypatch/ZipAPI/.venv/Scripts/python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
}

Write-Host "Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Testing API endpoints..." -ForegroundColor Green
Write-Host ""

# Function to make API requests with error handling
function Invoke-ApiRequest {
    param(
        [string]$Uri,
        [string]$Method = "GET",
        [hashtable]$Body = $null
    )
    
    try {
        if ($Body) {
            $bodyJson = $Body | ConvertTo-Json
            $response = Invoke-RestMethod -Uri $Uri -Method $Method -Body $bodyJson -ContentType "application/json" -TimeoutSec 5
        } else {
            $response = Invoke-RestMethod -Uri $Uri -Method $Method -TimeoutSec 5
        }
        return @{ Success = $true; Data = $response }
    } catch {
        return @{ Success = $false; Error = $_.Exception.Message }
    }
}

# 1. Health Check
Write-Host "1. Health Check:" -ForegroundColor Blue
$result = Invoke-ApiRequest -Uri "http://127.0.0.1:8000/health"
if ($result.Success) {
    Write-Host "   ✓ Status: $($result.Data.status)" -ForegroundColor Green
    Write-Host "   ✓ Service: $($result.Data.service)" -ForegroundColor Green
    Write-Host "   ✓ Version: $($result.Data.version)" -ForegroundColor Green
} else {
    Write-Host "   ✗ Health check failed: $($result.Error)" -ForegroundColor Red
}
Write-Host ""

# 2. API Root Information
Write-Host "2. API Information:" -ForegroundColor Blue
$result = Invoke-ApiRequest -Uri "http://127.0.0.1:8000/"
if ($result.Success) {
    Write-Host "   ✓ Message: $($result.Data.message)" -ForegroundColor Green
    Write-Host "   ✓ Version: $($result.Data.version)" -ForegroundColor Green
    Write-Host "   ✓ Documentation: http://127.0.0.1:8000$($result.Data.docs_url)" -ForegroundColor Green
} else {
    Write-Host "   ✗ Root endpoint failed: $($result.Error)" -ForegroundColor Red
}
Write-Host ""

# 3. Test ZipCode Density Assessment - Manhattan
Write-Host "3. Testing ZipCode 10001 (Manhattan):" -ForegroundColor Blue
$result = Invoke-ApiRequest -Uri "http://127.0.0.1:8000/api/v1/zipcode/density" -Method "POST" -Body @{ zipcode = "10001"; radius_miles = 25.0 }
if ($result.Success) {
    Write-Host "   ✓ ZipCode: $($result.Data.zipcode)" -ForegroundColor Green
    Write-Host "   ✓ Population Density: $([math]::Round($result.Data.population_density, 1)) people/sq mile" -ForegroundColor Green
    Write-Host "   ✓ Density Score: $($result.Data.density_score)/100" -ForegroundColor Green
    Write-Host "   ✓ National Percentile: $($result.Data.national_percentile)%" -ForegroundColor Green
    Write-Host "   ✓ Assessment: $($result.Data.assessment_summary)" -ForegroundColor Green
    
    if ($result.Data.nearby_comparison -and $result.Data.nearby_comparison.Count -gt 0) {
        Write-Host "   ✓ Nearby ZipCodes:" -ForegroundColor Green
        foreach ($nearby in $result.Data.nearby_comparison | Select-Object -First 3) {
            Write-Host "     • $($nearby.zipcode) ($($nearby.city), $($nearby.state)) - $($nearby.distance_miles) miles" -ForegroundColor Cyan
        }
    }
} else {
    Write-Host "   ✗ Density assessment failed: $($result.Error)" -ForegroundColor Red
}
Write-Host ""

# 4. Test ZipCode Density Assessment - Beverly Hills
Write-Host "4. Testing ZipCode 90210 (Beverly Hills):" -ForegroundColor Blue
$result = Invoke-ApiRequest -Uri "http://127.0.0.1:8000/api/v1/zipcode/density" -Method "POST" -Body @{ zipcode = "90210"; radius_miles = 25.0 }
if ($result.Success) {
    Write-Host "   ✓ ZipCode: $($result.Data.zipcode)" -ForegroundColor Green
    Write-Host "   ✓ Population Density: $([math]::Round($result.Data.population_density, 1)) people/sq mile" -ForegroundColor Green
    Write-Host "   ✓ Density Score: $($result.Data.density_score)/100" -ForegroundColor Green
    Write-Host "   ✓ National Percentile: $($result.Data.national_percentile)%" -ForegroundColor Green
    Write-Host "   ✓ Assessment: $($result.Data.assessment_summary)" -ForegroundColor Green
} else {
    Write-Host "   ✗ Density assessment failed: $($result.Error)" -ForegroundColor Red
}
Write-Host ""

# 5. Get Nearby ZipCodes
Write-Host "5. Getting nearby zipcodes for 10001:" -ForegroundColor Blue
$nearbyUri = "http://127.0.0.1:8000/api/v1/zipcode/10001/nearby?radius_miles=50" + "&" + "limit=5"
$result = Invoke-ApiRequest -Uri $nearbyUri
if ($result.Success -and $result.Data) {
    Write-Host "   ✓ Found $($result.Data.Count) nearby zipcodes:" -ForegroundColor Green
    foreach ($zip in $result.Data) {
        Write-Host "     • $($zip.zipcode) - $($zip.city), $($zip.state) ($([math]::Round($zip.distance_miles, 1)) miles, density: $([math]::Round($zip.population_density, 0)))" -ForegroundColor Cyan
    }
} else {
    Write-Host "   ✗ Nearby zipcodes failed: $($result.Error)" -ForegroundColor Red
}
Write-Host ""

# 6. Get ZipCode Statistics
Write-Host "6. ZipCode Statistics for 10001:" -ForegroundColor Blue
$result = Invoke-ApiRequest -Uri "http://127.0.0.1:8000/api/v1/zipcode/10001/stats"
if ($result.Success) {
    Write-Host "   ✓ ZipCode: $($result.Data.zipcode)" -ForegroundColor Green
    Write-Host "   ✓ City: $($result.Data.city)" -ForegroundColor Green
    Write-Host "   ✓ State: $($result.Data.state)" -ForegroundColor Green
    Write-Host "   ✓ Population: $($result.Data.population)" -ForegroundColor Green
    Write-Host "   ✓ Area: $($result.Data.area_sq_miles) sq miles" -ForegroundColor Green
    Write-Host "   ✓ Coordinates: $($result.Data.latitude), $($result.Data.longitude)" -ForegroundColor Green
} else {
    Write-Host "   ✗ Statistics failed: $($result.Error)" -ForegroundColor Red
}
Write-Host ""

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "CLI Command Reference:" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "PowerShell Commands:" -ForegroundColor Yellow
Write-Host "# Health Check" -ForegroundColor Gray
Write-Host 'Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"' -ForegroundColor White
Write-Host ""

Write-Host "# Assess ZipCode Density" -ForegroundColor Gray
Write-Host '$body = @{ zipcode = "10001"; radius_miles = 25.0 } | ConvertTo-Json' -ForegroundColor White
Write-Host 'Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/zipcode/density" -Method POST -Body $body -ContentType "application/json"' -ForegroundColor White
Write-Host ""

Write-Host "# Get Nearby ZipCodes" -ForegroundColor Gray
Write-Host 'Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/zipcode/10001/nearby?radius_miles=25&limit=5"' -ForegroundColor White
Write-Host ""

Write-Host "# Get ZipCode Statistics" -ForegroundColor Gray
Write-Host 'Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/zipcode/10001/stats"' -ForegroundColor White
Write-Host ""

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Demo Complete!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 Visit http://127.0.0.1:8000/docs for interactive documentation" -ForegroundColor Magenta
Write-Host "🏥 Visit http://127.0.0.1:8000/health to check API health" -ForegroundColor Magenta
Write-Host ""

# Cleanup
Write-Host "Stopping API server..." -ForegroundColor Yellow
Stop-Job -Job $serverJob -Force | Out-Null
Remove-Job -Job $serverJob -Force | Out-Null

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")