# ================================
# app/main.py
# ================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.core.config import settings
from app.database import Base, engine
from app.api.routes import properties, health, predict
from app.utils.responses import create_success_response
from app.core.ml_models import MLModelManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("Starting up application...")
    
    # Load ML models at startup
    try:
        model_manager = MLModelManager()
        await model_manager.load_models()
        logger.info("ML models loaded successfully at startup")
    except Exception as e:
        logger.error(f"Failed to load ML models at startup: {str(e)}")
        # You can choose to raise the exception to prevent startup
        # raise e
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")

# FastAPI App with lifespan management
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Realestica API - Real Estate Price Prediction & Management",
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(properties.router, prefix="/properties", tags=["Properties"])
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(predict.router, prefix="/predict", tags=["Price Prediction"])

@app.get("/", tags=["Root"])
async def root():
    return create_success_response({
        "message": settings.PROJECT_NAME, 
        "version": settings.PROJECT_VERSION,
        "description": "Real Estate Price Prediction & Management API",
        "endpoints": {
            "properties": "/properties",
            "health": "/health", 
            "prediction": "/predict",
            "docs": "/docs"
        }
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)