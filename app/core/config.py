import os
from typing import Optional

class Settings:
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL"
    )
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Realestica Property Management API"
    PROJECT_VERSION: str = "1.0.0"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]

settings = Settings()
