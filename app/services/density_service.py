import logging
from typing import Optional, List, Dict, Any
import numpy as np

from .data_service import DataService
from ..models.schemas import DensityResponse, NearbyComparison, ZipCodeStats

logger = logging.getLogger(__name__)

class DensityService:
    """Service for population density calculations and assessments"""
    
    def __init__(self, data_service: DataService):
        self.data_service = data_service
    
    async def assess_zipcode_density(
        self, 
        zipcode: str, 
        radius_miles: float = 25.0
    ) -> Optional[DensityResponse]:
        """
        Assess population density for a zipcode with relative comparisons
        """
        try:
            # Get zipcode data
            zipcode_info = self.data_service.get_zipcode_data(zipcode)
            if not zipcode_info:
                return None
            
            density = zipcode_info['population_density']
            lat, lon = zipcode_info['latitude'], zipcode_info['longitude']
            
            # Calculate national percentile
            national_percentile = self.data_service.calculate_percentile(
                density, 'population_density'
            )
            
            # Calculate normalized density score (0-100)
            density_score = self._calculate_density_score(density)
            
            # Get nearby zipcodes for comparison
            nearby_zipcodes = await self._get_nearby_comparisons(
                lat, lon, radius_miles, zipcode
            )
            
            # Generate assessment summary
            summary = self._generate_assessment_summary(
                density_score, national_percentile
            )
            
            return DensityResponse(
                zipcode=zipcode,
                population_density=round(density, 2),
                density_score=round(density_score, 1),
                national_percentile=round(national_percentile, 1),
                nearby_comparison=nearby_zipcodes,
                assessment_summary=summary
            )
            
        except Exception as e:
            logger.error(f"Error assessing density for zipcode {zipcode}: {e}")
            return None
    
    async def get_nearby_zipcodes(
        self, 
        zipcode: str, 
        radius_miles: float = 25.0,
        limit: int = 10
    ) -> List[NearbyComparison]:
        """Get nearby zipcodes with density comparisons"""
        try:
            zipcode_info = self.data_service.get_zipcode_data(zipcode)
            if not zipcode_info:
                return []
            
            lat, lon = zipcode_info['latitude'], zipcode_info['longitude']
            return await self._get_nearby_comparisons(lat, lon, radius_miles, zipcode, limit)
            
        except Exception as e:
            logger.error(f"Error getting nearby zipcodes for {zipcode}: {e}")
            return []
    
    async def get_zipcode_statistics(self, zipcode: str) -> Optional[ZipCodeStats]:
        """Get detailed statistics for a zipcode"""
        try:
            zipcode_info = self.data_service.get_zipcode_data(zipcode)
            if not zipcode_info:
                return None
            
            return ZipCodeStats(
                zipcode=zipcode,
                state=zipcode_info['state'],
                city=zipcode_info.get('city'),
                population=zipcode_info.get('population'),
                area_sq_miles=zipcode_info.get('area_sq_miles'),
                population_density=zipcode_info.get('population_density'),
                latitude=zipcode_info.get('latitude'),
                longitude=zipcode_info.get('longitude')
            )
            
        except Exception as e:
            logger.error(f"Error getting statistics for zipcode {zipcode}: {e}")
            return None
    
    def _calculate_density_score(self, density: float) -> float:
        """
        Calculate normalized density score (0-100) based on population density
        """
        # Get all densities for normalization
        all_data = self.data_service.get_all_zipcodes()
        max_density = all_data['population_density'].max()
        min_density = all_data['population_density'].min()
        
        # Normalize to 0-100 scale with logarithmic adjustment for better distribution
        if max_density == min_density:
            return 50.0  # If all densities are the same
        
        # Use log scale to better distribute scores
        log_density = np.log1p(density)  # log(1 + density) to handle zeros
        log_max = np.log1p(max_density)
        log_min = np.log1p(min_density)
        
        normalized = (log_density - log_min) / (log_max - log_min)
        return max(0.0, min(100.0, normalized * 100))
    
    async def _get_nearby_comparisons(
        self, 
        lat: float, 
        lon: float, 
        radius_miles: float,
        exclude_zipcode: str,
        limit: int = 5
    ) -> List[NearbyComparison]:
        """Get nearby zipcode comparisons"""
        try:
            nearby_df = await self.data_service.find_nearby_zipcodes(
                lat, lon, radius_miles, limit + 1  # +1 to account for excluding current zipcode
            )
            
            # Exclude the current zipcode
            nearby_df = nearby_df[nearby_df['zipcode'] != exclude_zipcode]
            
            # Sort by distance and limit results
            nearby_df = nearby_df.sort_values('distance_miles').head(limit)
            
            comparisons = []
            for _, row in nearby_df.iterrows():
                density_score = self._calculate_density_score(row['population_density'])
                
                comparison = NearbyComparison(
                    zipcode=row['zipcode'],
                    distance_miles=round(row['distance_miles'], 1),
                    population_density=round(row['population_density'], 2),
                    density_score=round(density_score, 1),
                    state=row['state'],
                    city=row.get('city')
                )
                comparisons.append(comparison)
            
            return comparisons
            
        except Exception as e:
            logger.error(f"Error getting nearby comparisons: {e}")
            return []
    
    def _generate_assessment_summary(
        self, 
        density_score: float, 
        national_percentile: float
    ) -> str:
        """Generate human-readable assessment summary"""
        if national_percentile >= 95:
            return "Extremely high density - Top 5% nationally"
        elif national_percentile >= 85:
            return "Very high density - Top 15% nationally"
        elif national_percentile >= 70:
            return "High density - Above 70th percentile"
        elif national_percentile >= 50:
            return "Above average density"
        elif national_percentile >= 30:
            return "Below average density"
        elif national_percentile >= 15:
            return "Low density - Bottom 30%"
        else:
            return "Very low density - Bottom 15% nationally"