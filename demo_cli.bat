@echo off
echo ====================================
echo ZipCode Population Density API Demo
echo ====================================
echo.

echo Starting API server in background...
start /B "ZipCodeAPI" cmd /c "C:/Users/rypatch/ZipAPI/.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

echo Waiting for server to start...
timeout /t 5 /nobreak > nul

echo.
echo Testing API endpoints...
echo.

echo 1. Health Check:
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health' -TimeoutSec 5; Write-Host '✓ Status:' $response.status; Write-Host '✓ Service:' $response.service } catch { Write-Host '✗ Health check failed' }"

echo.
echo 2. API Root Information:
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/' -TimeoutSec 5; Write-Host '✓ Message:' $response.message; Write-Host '✓ Version:' $response.version } catch { Write-Host '✗ Root endpoint failed' }"

echo.
echo 3. Testing ZipCode 10001 (Manhattan):
powershell -Command "$body = @{ zipcode = '10001'; radius_miles = 25.0 } | ConvertTo-Json; try { $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/zipcode/density' -Method POST -Body $body -ContentType 'application/json' -TimeoutSec 5; Write-Host '✓ ZipCode:' $response.zipcode; Write-Host '✓ Density:' $response.population_density 'people/sq mile'; Write-Host '✓ Score:' $response.density_score'/100'; Write-Host '✓ Percentile:' $response.national_percentile'%'; Write-Host '✓ Summary:' $response.assessment_summary } catch { Write-Host '✗ Density assessment failed' }"

echo.
echo 4. Testing ZipCode 90210 (Beverly Hills):
powershell -Command "$body = @{ zipcode = '90210'; radius_miles = 25.0 } | ConvertTo-Json; try { $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/zipcode/density' -Method POST -Body $body -ContentType 'application/json' -TimeoutSec 5; Write-Host '✓ ZipCode:' $response.zipcode; Write-Host '✓ Density:' $response.population_density 'people/sq mile'; Write-Host '✓ Score:' $response.density_score'/100'; Write-Host '✓ Percentile:' $response.national_percentile'%'; Write-Host '✓ Summary:' $response.assessment_summary } catch { Write-Host '✗ Density assessment failed' }"

echo.
echo 5. Getting nearby zipcodes for 10001:
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/v1/zipcode/10001/nearby?radius_miles=50&limit=3' -TimeoutSec 5; Write-Host '✓ Found' $response.Count 'nearby zipcodes:'; foreach($zip in $response) { Write-Host '  •' $zip.zipcode '-' $zip.city',' $zip.state '(' $zip.distance_miles 'miles, density:' $zip.population_density ')' } } catch { Write-Host '✗ Nearby zipcodes failed' }"

echo.
echo ====================================
echo Demo Complete!
echo ====================================
echo.
echo You can also visit: http://127.0.0.1:8000/docs
echo For interactive API documentation
echo.
echo To stop the server, press Ctrl+C or close this window
pause