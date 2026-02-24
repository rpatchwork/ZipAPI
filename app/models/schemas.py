from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from enum import Enum

class ZipCodeRequest(BaseModel):
    """Request model for zipcode density assessment"""
    zipcode: str = Field(..., description="5-digit US zipcode", min_length=5, max_length=5)
    radius_miles: Optional[float] = Field(25.0, description="Radius in miles for nearby comparison", gt=0, le=100)
    
    @field_validator('zipcode')
    @classmethod
    def validate_zipcode(cls, v):
        if not v.isdigit():
            raise ValueError('ZipCode must contain only digits')
        if len(v) != 5:
            raise ValueError('ZipCode must be exactly 5 digits')
        return v

class NearbyComparison(BaseModel):
    """Model for nearby zipcode comparison data"""
    zipcode: str
    distance_miles: float
    population_density: float
    density_score: float
    state: str
    city: Optional[str] = None

class DensityResponse(BaseModel):
    """Response model for zipcode density assessment"""
    zipcode: str
    population_density: float = Field(..., description="Population per square mile")
    density_score: float = Field(..., description="Normalized density score (0-100)")
    national_percentile: float = Field(..., description="Percentile rank among all continental USA zipcodes")
    nearby_comparison: List[NearbyComparison] = Field(..., description="Nearby zipcodes comparison")
    assessment_summary: str = Field(..., description="Human-readable assessment summary")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "zipcode": "10001",
                "population_density": 74781.2,
                "density_score": 95.8,
                "national_percentile": 99.2,
                "nearby_comparison": [
                    {
                        "zipcode": "10002",
                        "distance_miles": 1.2,
                        "population_density": 83426.1,
                        "density_score": 97.1,
                        "state": "NY",
                        "city": "New York"
                    }
                ],
                "assessment_summary": "Extremely high density - Top 1% nationally"
            }
        }
    )

class ZipCodeStats(BaseModel):
    """Detailed statistics for a zipcode"""
    zipcode: str
    state: str
    city: Optional[str]
    population: Optional[int]
    area_sq_miles: Optional[float]
    population_density: Optional[float]
    latitude: Optional[float]
    longitude: Optional[float]