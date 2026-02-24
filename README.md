# ZipCode Population Density Assessment API

[![Build and Deploy](https://github.com/rypatch/ZipAPI/actions/workflows/build-deploy.yml/badge.svg)](https://github.com/rypatch/ZipAPI/actions/workflows/build-deploy.yml)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io%2Frypatch%2Fzipcode--api-blue)](https://github.com/rypatch/ZipAPI/pkgs/container/zipcode-api)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A containerized Python FastAPI application that assesses zipcode population density and provides relative comparisons to nearby zipcodes and all continental USA zipcodes.

**🚀 Ready for Azure Windows VM deployment with automated startup configuration.**

## Features

- **Population Density Assessment**: Analyze population density for any US zipcode
- **Relative Comparisons**: Compare density with nearby zipcodes within a specified radius
- **National Rankings**: Get percentile rankings compared to all continental USA zipcodes
- **RESTful API**: FastAPI-based REST endpoints with automatic documentation
- **Containerized**: Docker support for easy deployment to virtual machines
- **Health Monitoring**: Built-in health checks and monitoring capabilities

## API Endpoints

### Core Endpoints

- `POST /api/v1/zipcode/density` - Assess population density for a zipcode
- `GET /api/v1/zipcode/{zipcode}/nearby` - Get nearby zipcodes with comparisons
- `GET /api/v1/zipcode/{zipcode}/stats` - Get detailed zipcode statistics
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

### Example Response

```json
{
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
```

## Quick Start

### 🐳 Container Deployment (Recommended for Production)

**Azure Windows VM Deployment:**
```powershell
# Download and run the automated deployment script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/YOUR_USERNAME/ZipAPI/main/deploy-windows.ps1" -OutFile "deploy.ps1"
PowerShell -ExecutionPolicy Bypass -File "deploy.ps1"
```

**Docker Hub / GitHub Container Registry:**
```bash
# Pull and run the container
docker pull ghcr.io/YOUR_USERNAME/zipcode-api:latest
docker run -d -p 80:8000 --name zipcode-api --restart unless-stopped ghcr.io/YOUR_USERNAME/zipcode-api:latest
```

📖 **[Full Deployment Guide](DEPLOYMENT.md)** - Complete instructions for Azure VM deployment

### Running with Docker (Recommended for VM deployment)

1. **Build and run the container**:
   ```bash
   docker build -t zipcode-api:latest .
   docker run -p 8000:8000 zipcode-api:latest
   ```

2. **Using Docker Compose**:
   ```bash
   docker-compose up --build
   ```

## 🚀 Production Deployment

### For Azure Windows VMs (Recommended)

**Quick Deployment**:
1. **Download and run the deployment script**:
   ```powershell
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/rypatch/ZipAPI/main/deploy-windows.ps1" -OutFile "deploy.ps1"
   PowerShell -ExecutionPolicy Bypass -File "deploy.ps1"
   ```

2. **The script will automatically**:
   - Install Docker Desktop (if needed)
   - Pull the latest container image
   - Configure automatic startup
   - Start the API service
   - Set up health monitoring

3. **Access your deployed API**:
   - API: http://localhost:8000
   - Health check: http://localhost:8000/health  
   - Documentation: http://localhost:8000/docs

**📖 Complete deployment guide**: [DEPLOYMENT.md](DEPLOYMENT.md)

**🐙 GitHub setup guide**: [GITHUB_SETUP.md](GITHUB_SETUP.md)

### Pre-Built Container Images

Pull the latest production-ready container:

```powershell
# Latest stable release
docker pull ghcr.io/rypatch/zipcode-api:latest

# Specific version
docker pull ghcr.io/rypatch/zipcode-api:v1.0.0

# Run directly
docker run -d --name zipcode-api -p 8000:8000 --restart unless-stopped ghcr.io/rypatch/zipcode-api:latest
```

### Development Setup

1. **Set up Python environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-test.txt  # For testing
   ```

3. **Run the development server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### VS Code Tasks

The project includes several VS Code tasks:

- **Start FastAPI Development Server**: Launch the API in development mode
- **Run Tests**: Execute the test suite
- **Build Docker Image**: Build the Docker container
- **Run Docker Container**: Build and run the containerized application
- **Start with Docker Compose**: Launch using docker-compose

Access tasks via `Ctrl+Shift+P` → `Tasks: Run Task`

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

## API Usage Examples

### Assess Zipcode Density

```bash
curl -X POST "http://localhost:8000/api/v1/zipcode/density" \
     -H "Content-Type: application/json" \
     -d '{
       "zipcode": "10001",
       "radius_miles": 25.0
     }'
```

### Get Nearby Zipcodes

```bash
curl "http://localhost:8000/api/v1/zipcode/10001/nearby?radius_miles=25&limit=10"
```

### Health Check

```bash
curl "http://localhost:8000/health"
```

## Data Requirements

**Note**: This demo includes sample data for testing. For production use, replace the sample data in `app/services/data_service.py` with actual zipcode data containing:

- `zipcode`: 5-digit US zipcode
- `state`: State abbreviation
- `city`: City name
- `latitude` / `longitude`: Geographic coordinates
- `population`: Population count
- `area_sq_miles`: Area in square miles

## Deployment to Virtual Machine

### Docker Deployment (Recommended)

1. **Copy files to your VM**
2. **Build and run**:
   ```bash
   docker-compose up --build -d
   ```

3. **Verify deployment**:
   ```bash
   curl http://your-vm-ip:8000/health
   ```

### Direct Python Deployment

1. **Install Python 3.11+ on your VM**
2. **Copy project files and install dependencies**
3. **Run with production WSGI server**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

## Configuration

Environment variables:

- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `LOG_LEVEL`: Logging level (default: INFO)

## Architecture

```
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── dependencies.py         # Dependency injection
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── routers/
│   │   └── zipcode.py         # API routes
│   └── services/
│       ├── data_service.py    # Data management
│       └── density_service.py # Population density calculations
├── tests/                     # Test suite
├── data/                     # Data files (replace with actual data)
├── Dockerfile               # Container configuration
├── docker-compose.yml      # Multi-container setup
└── requirements.txt        # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

- **API Documentation**: Visit `/docs` when running the server
- **Health Status**: Visit `/health` for application health
- **Issues**: Report issues on the project repository