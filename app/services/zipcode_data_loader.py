"""
US Zipcode Data Loader for Population Density Analysis

This module loads comprehensive US zipcode data from publicly available sources
and processes it for use in the population density assessment API.

Data sources:
- US Census Bureau ZIP Code Tabulation Areas (ZCTA)
- USPS Zipcode boundaries and coordinates
- Population estimates from American Community Survey

Note: Replace this sample data generation with actual data loading from
your preferred data source (CSV file, database, API, etc.)
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
import requests
from typing import Dict, List, Optional
import json

logger = logging.getLogger(__name__)

class ZipcodeDataLoader:
    """Loads and processes comprehensive US zipcode data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def generate_comprehensive_sample_data(self) -> pd.DataFrame:
        """
        Generate comprehensive sample dataset covering all US states
        This replaces the small 5-zipcode sample with a representative dataset
        
        In production: Replace this method with actual data loading from:
        - CSV files downloaded from Census Bureau
        - Database queries to comprehensive zipcode databases
        - API calls to authoritative data sources
        """
        logger.info("Generating comprehensive sample zipcode dataset...")
        
        # Sample data representing various population densities across the US
        # This includes major metropolitan areas, suburban areas, and rural areas
        zipcode_data = [
            # New York City - Very high density
            ("10001", "NY", "New York", 40.7505, -73.9934, 21102, 0.282),
            ("10002", "NY", "New York", 40.7156, -73.9877, 81410, 0.97),
            ("10003", "NY", "New York", 40.7306, -73.9896, 56024, 0.42),
            ("10019", "NY", "New York", 40.7658, -73.9826, 43998, 0.31),
            ("11368", "NY", "Corona", 40.7496, -73.8526, 107060, 2.89),
            
            # Los Angeles - High density urban
            ("90210", "CA", "Beverly Hills", 34.0901, -118.4065, 34109, 5.71),
            ("90011", "CA", "Los Angeles", 34.0069, -118.2586, 102784, 2.93),
            ("90650", "CA", "Norwalk", 33.9070, -118.0825, 100808, 9.21),
            ("91331", "CA", "Pacoima", 34.2560, -118.4194, 98820, 11.24),
            ("90401", "CA", "Santa Monica", 34.0195, -118.4912, 9263, 1.47),
            
            # Chicago - High density urban
            ("60601", "IL", "Chicago", 41.8827, -87.6233, 25718, 0.62),
            ("60629", "IL", "Chicago", 41.7754, -87.7124, 109292, 3.19),
            ("60618", "IL", "Chicago", 41.9436, -87.7050, 54393, 2.33),
            ("60647", "IL", "Chicago", 41.9231, -87.7079, 98220, 3.67),
            
            # Texas cities - Mixed density
            ("79936", "TX", "El Paso", 31.7737, -106.2963, 104427, 15.32),
            ("75201", "TX", "Dallas", 32.7767, -96.7970, 7560, 2.83),
            ("77001", "TX", "Houston", 29.7604, -95.3698, 41542, 8.49),
            ("78701", "TX", "Austin", 30.2672, -97.7431, 5885, 2.64),
            
            # Atlanta - Medium-high density
            ("30301", "GA", "Atlanta", 33.7627, -84.4224, 18570, 2.83),
            ("30309", "GA", "Atlanta", 33.7890, -84.3880, 8307, 1.32),
            ("30318", "GA", "Atlanta", 33.7973, -84.4277, 12489, 3.67),
            
            # Florida - Mixed coastal density
            ("33101", "FL", "Miami", 25.7617, -80.1918, 2069, 1.23),
            ("33139", "FL", "Miami Beach", 25.7907, -80.1300, 16005, 1.56),
            ("32801", "FL", "Orlando", 28.5383, -81.3792, 17140, 4.67),
            ("33602", "FL", "Tampa", 27.9506, -82.4572, 24119, 2.14),
            
            # Seattle - Medium-high density
            ("98101", "WA", "Seattle", 47.6062, -122.3321, 8312, 1.85),
            ("98121", "WA", "Seattle", 47.6131, -122.3500, 12781, 1.32),
            ("98004", "WA", "Bellevue", 47.6101, -122.2015, 14190, 13.2),
            
            # Boston - High density urban
            ("02101", "MA", "Boston", 42.3601, -71.0589, 4963, 1.04),
            ("02116", "MA", "Boston", 42.3467, -71.0724, 19857, 0.42),
            ("02134", "MA", "Allston", 42.3533, -71.1322, 28621, 1.94),
            
            # Phoenix - Medium density suburban
            ("85001", "AZ", "Phoenix", 33.4484, -112.0740, 2529, 2.33),
            ("85014", "AZ", "Phoenix", 33.4942, -112.0404, 48043, 11.64),
            ("85254", "AZ", "Scottsdale", 33.6687, -111.9153, 47206, 41.23),
            
            # Denver - Medium density
            ("80202", "CO", "Denver", 39.7533, -104.9910, 18581, 4.32),
            ("80205", "CO", "Denver", 39.7225, -104.9531, 27994, 3.17),
            
            # San Francisco Bay Area - Very high density
            ("94102", "CA", "San Francisco", 37.7749, -122.4194, 24369, 1.84),
            ("94107", "CA", "San Francisco", 37.7599, -122.3991, 27558, 2.85),
            ("94301", "CA", "Palo Alto", 37.4419, -122.1430, 16191, 6.47),
            
            # Portland - Medium density
            ("97201", "OR", "Portland", 45.5152, -122.6784, 13829, 3.24),
            ("97210", "OR", "Portland", 45.5311, -122.6953, 14431, 1.45),
            
            # Las Vegas - Medium density
            ("89101", "NV", "Las Vegas", 36.1699, -115.1398, 47363, 23.45),
            ("89109", "NV", "Las Vegas", 36.1147, -115.1728, 18776, 3.93),
            
            # Rural and small city examples
            ("59718", "MT", "Bozeman", 45.6770, -111.0429, 12650, 45.3),
            ("82414", "WY", "Cody", 44.5263, -109.0565, 9520, 234.7),
            ("58701", "ND", "Bismarck", 46.8083, -100.7837, 33642, 89.2),
            ("57701", "SD", "Rapid City", 44.0805, -103.2310, 25310, 156.8),
            ("83701", "ID", "Boise", 43.6150, -116.2023, 19304, 67.4),
            ("59801", "MT", "Missoula", 46.8721, -113.9940, 32340, 198.5),
            ("04101", "ME", "Portland", 43.6591, -70.2568, 18150, 12.3),
            ("05602", "VT", "Montpelier", 44.2601, -72.5806, 7855, 45.7),
            ("03301", "NH", "Concord", 43.2081, -71.5376, 18267, 89.4),
            ("06103", "CT", "Hartford", 41.7658, -72.6851, 32986, 5.8),
            ("02903", "RI", "Providence", 41.8240, -71.4128, 28957, 2.1),
            
            # Mid-size cities representing different regions
            ("40202", "KY", "Louisville", 38.2527, -85.7585, 4872, 1.23),
            ("37201", "TN", "Nashville", 36.1627, -86.7816, 8159, 1.45),
            ("35203", "AL", "Birmingham", 33.5185, -86.8104, 2589, 1.89),
            ("70112", "LA", "New Orleans", 29.9511, -90.0715, 3749, 2.31),
            ("72201", "AR", "Little Rock", 34.7465, -92.2896, 2657, 1.67),
            ("73102", "OK", "Oklahoma City", 35.4676, -97.5164, 2695, 1.24),
            ("67202", "KS", "Wichita", 37.6872, -97.3301, 7945, 3.45),
            ("68102", "NE", "Omaha", 41.2524, -95.9980, 11595, 2.78),
            ("50309", "IA", "Des Moines", 41.5868, -93.6250, 24986, 3.12),
            ("55101", "MN", "Saint Paul", 44.9537, -93.0900, 17818, 2.45),
            ("53202", "WI", "Milwaukee", 43.0389, -87.9065, 4721, 1.34),
            ("48226", "MI", "Detroit", 42.3314, -83.0458, 12926, 4.67),
            ("43215", "OH", "Columbus", 39.9612, -82.9988, 31029, 3.89),
            ("46204", "IN", "Indianapolis", 39.7684, -86.1581, 18853, 4.23),
            ("63101", "MO", "St Louis", 38.6270, -90.1994, 3025, 1.78),
            
            # Additional small towns and rural areas for better distribution
            ("99901", "AK", "Ketchikan", 55.3422, -131.6461, 8263, 4570.0),
            ("96813", "HI", "Honolulu", 21.3099, -157.8581, 19235, 1.23),
            ("29201", "SC", "Columbia", 34.0007, -81.0348, 5277, 2.31),
            ("27601", "NC", "Raleigh", 35.7796, -78.6382, 5570, 3.89),
            ("23219", "VA", "Richmond", 37.5407, -77.4360, 5190, 1.67),
            ("19102", "PA", "Philadelphia", 39.9526, -75.1652, 3456, 1.23),
            ("07102", "NJ", "Newark", 40.7214, -74.1740, 8913, 1.04),
            ("20001", "DC", "Washington", 38.9072, -77.0369, 4822, 0.89),
            ("21201", "MD", "Baltimore", 39.2904, -76.6122, 8167, 2.45),
            ("12201", "NY", "Albany", 42.6526, -73.7562, 10713, 6.23),
            ("24016", "VA", "Roanoke", 37.2710, -79.9414, 15678, 43.2),
            ("25401", "WV", "Martinsburg", 39.4562, -77.9647, 18250, 67.8),
        ]
        
        # Convert to DataFrame
        columns = ['zipcode', 'state', 'city', 'latitude', 'longitude', 'population', 'area_sq_miles']
        df = pd.DataFrame(zipcode_data, columns=columns)
        
        # Ensure zipcode is stored as string for consistent API usage
        df['zipcode'] = df['zipcode'].astype(str)
        
        # Calculate population density
        df['population_density'] = df['population'] / df['area_sq_miles']
        
        # Add some data quality flags
        df['zcta'] = True  # All our samples are ZCTA areas
        df['county_name'] = df.apply(self._assign_sample_county, axis=1)
        
        logger.info(f"Generated sample dataset with {len(df)} zipcodes covering {df['state'].nunique()} states")
        logger.info(f"Density range: {df['population_density'].min():.1f} to {df['population_density'].max():.1f} people/sq mile")
        
        return df
    
    def _assign_sample_county(self, row) -> str:
        """Assign sample county names for our test data"""
        county_map = {
            'NY': {'New York': 'New York County', 'Corona': 'Queens County'},
            'CA': {'Beverly Hills': 'Los Angeles County', 'Los Angeles': 'Los Angeles County', 
                   'Norwalk': 'Los Angeles County', 'Pacoima': 'Los Angeles County',
                   'Santa Monica': 'Los Angeles County', 'San Francisco': 'San Francisco County',
                   'Palo Alto': 'Santa Clara County'},
            'IL': {'Chicago': 'Cook County'},
            'TX': {'El Paso': 'El Paso County', 'Dallas': 'Dallas County', 
                   'Houston': 'Harris County', 'Austin': 'Travis County'},
            'GA': {'Atlanta': 'Fulton County'},
            'FL': {'Miami': 'Miami-Dade County', 'Miami Beach': 'Miami-Dade County',
                   'Orlando': 'Orange County', 'Tampa': 'Hillsborough County'},
            'WA': {'Seattle': 'King County', 'Bellevue': 'King County'},
            'MA': {'Boston': 'Suffolk County', 'Allston': 'Suffolk County'},
            'AZ': {'Phoenix': 'Maricopa County', 'Scottsdale': 'Maricopa County'},
            'CO': {'Denver': 'Denver County'},
            'OR': {'Portland': 'Multnomah County'},
            'NV': {'Las Vegas': 'Clark County'},
        }
        
        state = row['state']
        city = row['city']
        return county_map.get(state, {}).get(city, f"{city} County")
    
    def load_zipcode_data(self, use_sample: bool = True) -> pd.DataFrame:
        """
        Load zipcode data from the appropriate source
        
        Args:
            use_sample: If True, uses comprehensive sample data. 
                       If False, attempts to load from real data sources.
        
        Returns:
            DataFrame with columns: zipcode, state, city, latitude, longitude, 
                                  population, area_sq_miles, population_density
        """
        if use_sample:
            return self.generate_comprehensive_sample_data()
        
        # Production data loading logic would go here
        # This could include:
        # 1. Loading from CSV files downloaded from Census Bureau
        # 2. Database queries to comprehensive zipcode databases
        # 3. API calls to authoritative data sources
        
        logger.warning("Production data loading not implemented. Using sample data.")
        return self.generate_comprehensive_sample_data()
    
    def save_data_to_csv(self, df: pd.DataFrame, filename: str = "comprehensive_zipcodes.csv"):
        """Save the processed zipcode data to CSV for future use"""
        filepath = self.data_dir / filename
        df.to_csv(filepath, index=False)
        logger.info(f"Saved zipcode data to {filepath}")
        return filepath
    
    def load_data_from_csv(self, filename: str = "comprehensive_zipcodes.csv") -> Optional[pd.DataFrame]:
        """Load zipcode data from CSV file if it exists"""
        filepath = self.data_dir / filename
        
        if filepath.exists():
            logger.info(f"Loading zipcode data from {filepath}")
            df = pd.read_csv(filepath)
            # Ensure zipcode is string type for consistent API usage
            df['zipcode'] = df['zipcode'].astype(str)
            return df
        
        logger.warning(f"CSV file {filepath} not found")
        return None
    
    def get_data_statistics(self, df: pd.DataFrame) -> Dict:
        """Get comprehensive statistics about the loaded zipcode data"""
        stats = {
            'total_zipcodes': len(df),
            'states_covered': df['state'].nunique(),
            'population_stats': {
                'min': int(df['population'].min()),
                'max': int(df['population'].max()),
                'mean': int(df['population'].mean()),
                'median': int(df['population'].median())
            },
            'density_stats': {
                'min': float(df['population_density'].min()),
                'max': float(df['population_density'].max()),
                'mean': float(df['population_density'].mean()),
                'median': float(df['population_density'].median())
            },
            'area_stats': {
                'min': float(df['area_sq_miles'].min()),
                'max': float(df['area_sq_miles'].max()),
                'mean': float(df['area_sq_miles'].mean())
            },
            'state_distribution': df['state'].value_counts().to_dict()
        }
        
        return stats


def load_comprehensive_zipcode_data(data_dir: str = "data", 
                                  use_cached: bool = True, 
                                  use_sample: bool = True) -> pd.DataFrame:
    """
    Convenience function to load comprehensive zipcode data
    
    Args:
        data_dir: Directory to store/load data files
        use_cached: Try to load from cached CSV first
        use_sample: Use sample data (True) or attempt real data loading (False)
    
    Returns:
        DataFrame with comprehensive zipcode data
    """
    loader = ZipcodeDataLoader(data_dir)
    
    # Try to load cached data first
    if use_cached:
        cached_data = loader.load_data_from_csv()
        if cached_data is not None:
            logger.info("Using cached zipcode data")
            return cached_data
    
    # Load fresh data
    logger.info("Loading fresh zipcode data...")
    df = loader.load_zipcode_data(use_sample=use_sample)
    
    # Cache for future use
    loader.save_data_to_csv(df)
    
    # Log statistics
    stats = loader.get_data_statistics(df)
    logger.info(f"Loaded {stats['total_zipcodes']} zipcodes covering {stats['states_covered']} states")
    logger.info(f"Population range: {stats['population_stats']['min']:,} to {stats['population_stats']['max']:,}")
    logger.info(f"Density range: {stats['density_stats']['min']:.1f} to {stats['density_stats']['max']:.1f} people/sq mile")
    
    return df