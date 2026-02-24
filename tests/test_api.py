import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock

from app.main import app
from app.services.data_service import DataService
from app.services.density_service import DensityService
from app import dependencies

# Override dependencies for testing
def get_test_data_service():
    mock_service = MagicMock(spec=DataService)
    mock_service.is_initialized = True
    mock_service.get_zipcode_data.return_value = {
        'zipcode': '10001',
        'state': 'NY',
        'city': 'New York',
        'latitude': 40.7505,
        'longitude': -73.9934,
        'population': 21102,
        'area_sq_miles': 0.282,
        'population_density': 74865.25
    }
    return mock_service

def get_test_density_service():
    mock_service = MagicMock(spec=DensityService)
    return mock_service

# Apply overrides
app.dependency_overrides[dependencies.get_data_service] = get_test_data_service
app.dependency_overrides[dependencies.get_density_service] = get_test_density_service

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "zipcode-population-density-api"

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "ZipCode Population Density Assessment API" in data["message"]
    assert "version" in data

def test_zipcode_validation():
    """Test zipcode validation"""
    # Test invalid zipcode
    invalid_request = {"zipcode": "1234", "radius_miles": 25.0}
    response = client.post("/api/v1/zipcode/density", json=invalid_request)
    assert response.status_code == 422  # Validation error

    # Test non-numeric zipcode
    invalid_request = {"zipcode": "abcde", "radius_miles": 25.0}
    response = client.post("/api/v1/zipcode/density", json=invalid_request)
    assert response.status_code == 422  # Validation error