from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from .routers import zipcode
from .services.data_service import DataService
from .services.density_service import DensityService
from . import dependencies

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up ZipCode Population Density API")
    
    # Initialize data service
    data_service = DataService()
    await data_service.initialize()
    
    # Initialize density service
    density_service = DensityService(data_service)
    
    # Set global service instances
    dependencies.set_services(data_service, density_service)
    
    logger.info("All services initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down ZipCode Population Density API")

app = FastAPI(
    title="ZipCode Population Density Assessment API",
    description="API for assessing zipcode population density and providing relative comparisons",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(zipcode.router, prefix="/api/v1", tags=["zipcode"])

@app.get("/health")
async def health_check():
    """Health check endpoint for container monitoring"""
    return {
        "status": "healthy",
        "service": "zipcode-population-density-api",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "ZipCode Population Density Assessment API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_check": "/health"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception handler caught: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )