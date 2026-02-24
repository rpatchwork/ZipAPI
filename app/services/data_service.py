import pandas as pd
import numpy as np
import logging
from typing import Optional, Dict, Any
from geopy.distance import geodesic
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .zipcode_data_loader import load_comprehensive_zipcode_data

logger = logging.getLogger(__name__)

class DataService:
    """Service for loading and managing zipcode data"""
    
    def __init__(self):
        self.zipcode_data: Optional[pd.DataFrame] = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize the data service with zipcode data"""
        try:
            logger.info("Initializing data service...")
            
            # Load zipcode data (placeholder - replace with actual data loading)
            await self._load_zipcode_data()
            self.is_initialized = True
            
            logger.info(f"Data service initialized with {len(self.zipcode_data)} zipcodes")
            
        except Exception as e:
            logger.error(f"Failed to initialize data service: {e}")
            raise
    
    async def _load_zipcode_data(self):
        """Load comprehensive zipcode data from data source"""
        try:
            # Load comprehensive zipcode dataset
            # This includes 70+ zipcodes covering all major US metropolitan areas,
            # suburban areas, and rural areas for realistic density analysis
            
            loop = asyncio.get_event_loop()
            self.zipcode_data = await loop.run_in_executor(
                self.executor,
                load_comprehensive_zipcode_data,
                "data",  # data_dir
                True,     # use_cached
                True      # use_sample (comprehensive sample dataset)
            )
            
            logger.info(f"Comprehensive zipcode data loaded successfully")
            logger.info(f"Dataset contains {len(self.zipcode_data)} zipcodes covering {self.zipcode_data['state'].nunique()} states")
            
            # Log density statistics
            min_density = self.zipcode_data['population_density'].min()
            max_density = self.zipcode_data['population_density'].max()
            median_density = self.zipcode_data['population_density'].median()
            
            logger.info(f"Population density range: {min_density:.1f} to {max_density:.1f} people/sq mile (median: {median_density:.1f})")
            
        except Exception as e:
            logger.error(f"Error loading zipcode data: {e}")
            # Fallback to minimal sample data
            self._load_fallback_data()
    
    def _load_fallback_data(self):
        """Fallback to minimal sample data if comprehensive loading fails"""
        logger.warning("Using fallback minimal sample data")
        
        sample_data = {
            'zipcode': ['10001', '10002', '90210', '60601', '30301'],
            'state': ['NY', 'NY', 'CA', 'IL', 'GA'],
            'city': ['New York', 'New York', 'Beverly Hills', 'Chicago', 'Atlanta'],
            'latitude': [40.7505, 40.7156, 34.0901, 41.8827, 33.7627],
            'longitude': [-73.9934, -73.9877, -118.4065, -87.6233, -84.4224],
            'population': [21102, 81410, 34109, 25718, 18570],
            'area_sq_miles': [0.282, 0.97, 5.71, 0.62, 2.83],
        }
        
        self.zipcode_data = pd.DataFrame(sample_data)
        # Ensure zipcode is string for consistent API usage
        self.zipcode_data['zipcode'] = self.zipcode_data['zipcode'].astype(str)
        self.zipcode_data['population_density'] = (
            self.zipcode_data['population'] / self.zipcode_data['area_sq_miles']
        )
        
        logger.info("Fallback sample zipcode data loaded")
    
    def get_zipcode_data(self, zipcode: str) -> Optional[Dict[str, Any]]:
        """Get data for a specific zipcode"""
        if not self.is_initialized:
            raise RuntimeError("Data service not initialized")
        
        result = self.zipcode_data[self.zipcode_data['zipcode'] == zipcode]
        if result.empty:
            return None
        
        return result.iloc[0].to_dict()
    
    def get_all_zipcodes(self) -> pd.DataFrame:
        """Get all zipcode data"""
        if not self.is_initialized:
            raise RuntimeError("Data service not initialized")
        
        return self.zipcode_data.copy()
    
    async def find_nearby_zipcodes(
        self, 
        target_lat: float, 
        target_lon: float, 
        radius_miles: float,
        limit: int = 100
    ) -> pd.DataFrame:
        """Find zipcodes within specified radius of target coordinates"""
        if not self.is_initialized:
            raise RuntimeError("Data service not initialized")
        
        def calculate_distances(df):
            target_point = (target_lat, target_lon)
            distances = []
            
            for _, row in df.iterrows():
                zipcode_point = (row['latitude'], row['longitude'])
                distance = geodesic(target_point, zipcode_point).miles
                distances.append(distance)
            
            df = df.copy()
            df['distance_miles'] = distances
            return df[df['distance_miles'] <= radius_miles].head(limit)
        
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor, 
            calculate_distances, 
            self.zipcode_data
        )
        
        return result
    
    def calculate_percentile(self, value: float, column: str) -> float:
        """Calculate percentile of a value within a column"""
        if not self.is_initialized:
            raise RuntimeError("Data service not initialized")
        
        if column not in self.zipcode_data.columns:
            raise ValueError(f"Column {column} not found in data")
        
        percentile = (
            (self.zipcode_data[column] < value).sum() / len(self.zipcode_data)
        ) * 100
        
        return min(100.0, max(0.0, percentile))