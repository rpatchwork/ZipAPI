#!/usr/bin/env python3
"""
ZipCode Population Density API Demo Script

This script demonstrates how to interact with the ZipCode Population Density API
using Python's requests library. Run this while the API server is running.
"""

import requests
import json
import sys
import time
from typing import Dict, Any

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def make_request(method: str, endpoint: str, data: Dict[Any, Any] = None) -> Dict[Any, Any]:
    """Make an API request and handle errors"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError:
        print(f"❌ ERROR: Could not connect to API at {url}")
        print("   Make sure the server is running: uvicorn app.main:app --host 127.0.0.1 --port 8000")
        return None
    except requests.exceptions.Timeout:
        print(f"❌ ERROR: Request timed out to {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Request failed: {e}")
        return None

def test_health_check():
    """Test the health check endpoint"""
    print_section("1. Health Check")
    
    result = make_request("GET", "/health")
    if result:
        print("✅ API is healthy!")
        print(f"   Service: {result.get('service')}")
        print(f"   Status: {result.get('status')}")
        print(f"   Version: {result.get('version')}")
        return True
    return False

def test_root_endpoint():
    """Test the root endpoint"""
    print_section("2. API Information")
    
    result = make_request("GET", "/")
    if result:
        print("✅ API Root Information:")
        print(f"   Message: {result.get('message')}")
        print(f"   Version: {result.get('version')}")
        print(f"   Documentation: {API_BASE_URL}{result.get('docs_url')}")

def demo_zipcode_assessment():
    """Demonstrate zipcode density assessment"""
    print_section("3. ZipCode Density Assessment Demo")
    
    # Test zipcodes with different characteristics
    test_cases = [
        {"zipcode": "10001", "description": "Manhattan, NY (High density)"},
        {"zipcode": "90210", "description": "Beverly Hills, CA (Medium-high density)"},
        {"zipcode": "60601", "description": "Chicago, IL (High density)"},
        {"zipcode": "30301", "description": "Atlanta, GA (Medium density)"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📍 Test Case {i}: {test_case['description']}")
        print(f"   ZipCode: {test_case['zipcode']}")
        
        # Test density assessment
        request_data = {
            "zipcode": test_case["zipcode"],
            "radius_miles": 25.0
        }
        
        result = make_request("POST", "/api/v1/zipcode/density", request_data)
        
        if result:
            print("✅ Assessment Results:")
            print(f"   Population Density: {result.get('population_density'):,.1f} people/sq mile")
            print(f"   Density Score: {result.get('density_score')}/100")
            print(f"   National Percentile: {result.get('national_percentile')}%")
            print(f"   Assessment: {result.get('assessment_summary')}")
            
            # Show nearby comparisons
            nearby = result.get('nearby_comparison', [])
            if nearby:
                print(f"   Nearby ZipCodes ({len(nearby)}):")
                for neighbor in nearby[:3]:  # Show first 3
                    print(f"     • {neighbor['zipcode']} ({neighbor['city']}, {neighbor['state']}) - "
                          f"{neighbor['distance_miles']} miles - {neighbor['population_density']:,.0f} density")
        else:
            print(f"❌ Failed to assess zipcode {test_case['zipcode']}")

def demo_nearby_zipcodes():
    """Demonstrate nearby zipcode search"""
    print_section("4. Nearby ZipCodes Demo")
    
    zipcode = "10001"  # Manhattan
    print(f"📍 Finding zipcodes near {zipcode} within 50 miles")
    
    result = make_request("GET", f"/api/v1/zipcode/{zipcode}/nearby?radius_miles=50&limit=5")
    
    if result and result:
        print(f"✅ Found {len(result)} nearby zipcodes:")
        for neighbor in result:
            print(f"   • {neighbor['zipcode']} - {neighbor.get('city', 'Unknown')}, {neighbor['state']}")
            print(f"     Distance: {neighbor['distance_miles']} miles")
            print(f"     Density: {neighbor['population_density']:,.1f} people/sq mile")
            print(f"     Score: {neighbor['density_score']}/100")
            print()

def demo_zipcode_stats():
    """Demonstrate detailed zipcode statistics"""
    print_section("5. ZipCode Statistics Demo")
    
    zipcode = "10001"
    print(f"📊 Detailed statistics for ZipCode {zipcode}")
    
    result = make_request("GET", f"/api/v1/zipcode/{zipcode}/stats")
    
    if result:
        print("✅ Detailed Statistics:")
        print(f"   ZipCode: {result.get('zipcode')}")
        print(f"   City: {result.get('city', 'N/A')}")
        print(f"   State: {result.get('state')}")
        print(f"   Population: {result.get('population', 'N/A'):,}")
        print(f"   Area: {result.get('area_sq_miles', 'N/A')} square miles")
        print(f"   Density: {result.get('population_density', 'N/A'):,.1f} people/sq mile")
        print(f"   Coordinates: {result.get('latitude', 'N/A')}, {result.get('longitude', 'N/A')}")

def show_cli_commands():
    """Show equivalent CLI commands"""
    print_section("6. CLI Commands Reference")
    
    print("🔧 You can also test the API directly from command line:")
    print()
    
    # PowerShell commands
    print("PowerShell Commands:")
    print('   # Health Check')
    print('   Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" | ConvertTo-Json')
    print()
    print('   # Assess ZipCode Density')
    print('   $body = @{ zipcode = "10001"; radius_miles = 25.0 } | ConvertTo-Json')
    print('   Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/zipcode/density" -Method POST -Body $body -ContentType "application/json"')
    print()
    print('   # Get Nearby ZipCodes')
    print('   Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/zipcode/10001/nearby?radius_miles=25&limit=5"')
    print()
    
    # Curl commands (if available)
    print("Curl Commands (if curl is available):")
    print('   # Health Check')
    print('   curl "http://127.0.0.1:8000/health"')
    print()
    print('   # Assess ZipCode Density')
    print('   curl -X POST "http://127.0.0.1:8000/api/v1/zipcode/density" \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"zipcode": "10001", "radius_miles": 25.0}\'')

def main():
    """Run the complete demo"""
    print("🎯 ZipCode Population Density API Demo")
    print("=====================================")
    print(f"API Server: {API_BASE_URL}")
    print(f"Documentation: {API_BASE_URL}/docs")
    
    # Test if server is running
    if not test_health_check():
        print("\n⚠️  Please start the API server first:")
        print("   cd C:\\Users\\rypatch\\ZipAPI")
        print("   C:/Users/rypatch/ZipAPI/.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000")
        sys.exit(1)
    
    # Run all demo sections
    test_root_endpoint()
    demo_zipcode_assessment()
    demo_nearby_zipcodes()
    demo_zipcode_stats()
    show_cli_commands()
    
    print_section("Demo Complete!")
    print("🎉 All API endpoints tested successfully!")
    print(f"📖 Visit {API_BASE_URL}/docs for interactive documentation")

if __name__ == "__main__":
    main()