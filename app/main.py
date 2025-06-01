# ================================
# app/main.py
# ================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import Base, engine
from app.api.routes import properties, health
from app.utils.responses import create_success_response

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Simple CRUD API for Property Management",
    version=settings.PROJECT_VERSION
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(properties.router, prefix="/properties", tags=["Properties"])
app.include_router(health.router, prefix="/health", tags=["Health"])

@app.get("/", tags=["Root"])
async def root():
    return create_success_response({
        "message": settings.PROJECT_NAME, 
        "version": settings.PROJECT_VERSION
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)