# ================================
# app/api/routes/predict.py 
# ================================
from fastapi import APIRouter, HTTPException
import logging
from app.utils.responses import create_success_response, create_error_response
from app.core.ml_models import MLModelManager
from app.schemas import PropertyFeatures
from app.utils.responses import format_currency
logger = logging.getLogger(__name__)
router = APIRouter()

# Get model manager instance
model_manager = MLModelManager()

@router.post("/", response_model=dict, summary="Prediksi Harga Properti")
async def predict_property_price(features: PropertyFeatures):
    """
    Prediksi harga properti berdasarkan fitur-fitur yang diberikan.
    
    - **features**: Data properti yang akan diprediksi harganya
    
    Returns prediksi harga dalam Rupiah beserta status prediksi.
    """
    try:
        # Check if models are loaded
        if not model_manager.is_loaded():
            raise HTTPException(status_code=503, detail="ML models not loaded yet")
        
        # Preprocess data
        preprocessed_data = model_manager.preprocess_data(features.dict())
        
        # Predict
        predicted_price = model_manager.predict(preprocessed_data)
        
        # Format response
        response_data = {
            "prediksi_harga": predicted_price,
            "prediksi_harga_formatted": format_currency(predicted_price)
        }
        
        return create_success_response(data=response_data)
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        return create_error_response(message=f"Error during prediction: {str(e)}")

@router.get("/model-info", summary="Informasi Model")
async def get_model_info():
    """
    Mendapatkan informasi tentang model yang digunakan untuk prediksi.
    """
    try:
        model_info = {
            "model_loaded": model_manager.is_loaded(),
            "available_kabupaten": model_manager.get_available_kabupaten(),
            "available_sertifikat": model_manager.get_available_sertifikat(),
            "total_features": 39,
            "model_source": "stevencmichael/Capstone_Project_SM079-LAI"
        }
        
        return create_success_response(data=model_info)
        
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return create_error_response(message=f"Error getting model info: {str(e)}")
