# ================================
# app/api/routes/health.py
# ================================
from fastapi import APIRouter
from datetime import datetime
from app.utils.responses import create_success_response

router = APIRouter()

@router.get("/")
async def health_check():
    return create_success_response({
        "status": "healthy", 
        "timestamp": datetime.utcnow()
    })