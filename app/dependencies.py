from fastapi import Depends
import logging

from .services.data_service import DataService
from .services.density_service import DensityService

logger = logging.getLogger(__name__)

# Global instances (initialized in main.py lifespan)
_data_service: DataService = None
_density_service: DensityService = None

def get_data_service() -> DataService:
    """Dependency to get the data service instance"""
    global _data_service
    if _data_service is None:
        # Initialize if not already done (fallback)
        _data_service = DataService()
        logger.warning("Data service not initialized through lifespan - initializing now")
    return _data_service

def get_density_service() -> DensityService:
    """Dependency to get the density service instance"""
    global _density_service
    if _density_service is None:
        data_service = get_data_service()
        _density_service = DensityService(data_service)
        logger.warning("Density service not initialized through lifespan - initializing now")
    return _density_service

def set_services(data_service: DataService, density_service: DensityService):
    """Set service instances (called from main.py lifespan)"""
    global _data_service, _density_service
    _data_service = data_service
    _density_service = density_service