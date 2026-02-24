from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
import logging

from ..services.density_service import DensityService
from ..models.schemas import ZipCodeRequest, DensityResponse, NearbyComparison
from ..dependencies import get_density_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/zipcode/density", response_model=DensityResponse)
async def assess_density(
    request: ZipCodeRequest,
    density_service: DensityService = Depends(get_density_service)
):
    """
    Assess population density for a given zipcode and return relative comparisons.
    
    Returns:
    - density_score: Normalized density score (0-100)
    - national_percentile: Percentile rank compared to all continental USA zipcodes
    - nearby_comparison: Comparison with nearby zipcodes within specified radius
    - population_density: Actual population per square mile
    """
    try:
        logger.info(f"Processing density assessment for zipcode: {request.zipcode}")
        
        result = await density_service.assess_zipcode_density(
            zipcode=request.zipcode,
            radius_miles=request.radius_miles
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ZipCode {request.zipcode} not found or has no population data"
            )
        
        return result
        
    except ValueError as e:
        logger.warning(f"Invalid zipcode format: {request.zipcode}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error processing zipcode {request.zipcode}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing zipcode density assessment"
        )

@router.get("/zipcode/{zipcode}/nearby", response_model=List[NearbyComparison])
async def get_nearby_zipcodes(
    zipcode: str,
    radius_miles: Optional[float] = 25.0,
    limit: Optional[int] = 10,
    density_service: DensityService = Depends(get_density_service)
):
    """
    Get nearby zipcodes with their population density comparisons.
    """
    try:
        logger.info(f"Getting nearby zipcodes for: {zipcode}")
        
        nearby = await density_service.get_nearby_zipcodes(
            zipcode=zipcode,
            radius_miles=radius_miles,
            limit=limit
        )
        
        if not nearby:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No nearby zipcodes found for {zipcode}"
            )
        
        return nearby
        
    except Exception as e:
        logger.error(f"Error getting nearby zipcodes for {zipcode}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving nearby zipcodes"
        )

@router.get("/zipcode/{zipcode}/stats")
async def get_zipcode_stats(
    zipcode: str,
    density_service: DensityService = Depends(get_density_service)
):
    """
    Get detailed statistics for a specific zipcode.
    """
    try:
        stats = await density_service.get_zipcode_statistics(zipcode)
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ZipCode {zipcode} not found"
            )
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting stats for zipcode {zipcode}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving zipcode statistics"
        )