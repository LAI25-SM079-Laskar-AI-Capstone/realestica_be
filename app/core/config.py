# ================================
# app/core/config.py
# ================================
import os
from typing import Optional

class Settings:
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres.wodlrtysmleajqytwbnu:CbM8qZp3W3K1zYpm@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
    )
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Property Management API"
    PROJECT_VERSION: str = "1.0.0"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]

settings = Settings()
