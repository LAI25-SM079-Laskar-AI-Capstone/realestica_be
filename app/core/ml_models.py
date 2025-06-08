# ================================
# app/core/ml_models.py 
# ================================
import joblib
import pandas as pd
import numpy as np
from huggingface_hub import hf_hub_download
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class MLModelManager:
    """Singleton class untuk mengelola ML models"""
    _instance = None
    _models_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLModelManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.le_kabupaten = None
            self.le_sertifikat = None
            self.scaler = None
            self.model = None
            self.feature_columns = [
                'f_taman', 'f_jogging_track', 'f_cctv', 'f_lapangan_voli', 'f_lapangan_bola',
                'f_lapangan_basket', 'f_lapangan_bulu_tangkis', 'f_tempat_jemuran', 'f_kulkas',
                'f_telepon', 'f_tempat_cuci', 'f_laundry', 'f_masjid', 'f_taman_bermain',
                'f_kolam_renang', 'f_mesin_cuci', 'f_kompor', 'f_keamanan_24_jam', 'f_kolam_ikan',
                'f_backyard', 'f_kitchen_set', 'f_teras', 'f_wastafel', 'f_akses_parkir',
                'f_lapangan_tenis', 'f_tempat_gym', 'f_ac', 'f_water_heater', 'f_one_gate_system',
                's_jumlah_lantai', 's_kamar_mandi', 's_kamar_tidur', 's_luas_bangunan', 's_luas_tanah',
                'poi_perbelanjaan', 'poi_sekolah', 'poi_transportasi',
                'kabupaten_encoded', 's_sertifikat_encoded'
            ]
            self.initialized = True
    
    async def load_models(self):
        """Load semua model ML secara asinkron"""
        if self._models_loaded:
            return
            
        try:
            logger.info("Loading ML models from Hugging Face Hub...")
            
            # Download semua file sekaligus
            repo_id = "stevencmichael/Capstone_Project_SM079-LAI"
            
            # Download files
            le_kabupaten_path = hf_hub_download(repo_id, "le_kabupaten.joblib")
            le_sertifikat_path = hf_hub_download(repo_id, "le_sertifikat.joblib")
            scaler_path = hf_hub_download(repo_id, "standard_scaler.joblib")
            model_path = hf_hub_download(repo_id, "model.joblib")

            # Load semua model
            self.le_kabupaten = joblib.load(le_kabupaten_path)
            self.le_sertifikat = joblib.load(le_sertifikat_path)
            self.scaler = joblib.load(scaler_path)
            self.model = joblib.load(model_path)
            
            self._models_loaded = True
            logger.info("ML models loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading ML models: {str(e)}")
            raise RuntimeError(f"Failed to load ML models: {str(e)}")
    
    def is_loaded(self) -> bool:
        """Check apakah model sudah dimuat"""
        return self._models_loaded
    
    def get_available_kabupaten(self) -> List[str]:
        """Dapatkan daftar kabupaten yang tersedia"""
        if not self._models_loaded:
            return []
        return list(self.le_kabupaten.classes_)
    
    def get_available_sertifikat(self) -> List[str]:
        """Dapatkan daftar sertifikat yang tersedia"""
        if not self._models_loaded:
            return []
        return list(self.le_sertifikat.classes_)
    
    def preprocess_data(self, data: Dict) -> np.ndarray:
        """Preprocess data untuk prediksi"""
        if not self._models_loaded:
            raise RuntimeError("Models not loaded yet")
        
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Preprocess string columns
        df['kabupaten'] = df['kabupaten'].str.lower().str.strip()
        df['s_sertifikat'] = df['s_sertifikat'].str.lower().str.strip()
        
        # Handle unknown values
        known_kabupaten = self.le_kabupaten.classes_
        if df.loc[0, 'kabupaten'] not in known_kabupaten:
            logger.warning(f"Unknown kabupaten: {df.loc[0, 'kabupaten']}, using default")
            df.loc[0, 'kabupaten'] = known_kabupaten[0]
        
        known_sertifikat = self.le_sertifikat.classes_
        if df.loc[0, 's_sertifikat'] not in known_sertifikat:
            logger.warning(f"Unknown sertifikat: {df.loc[0, 's_sertifikat']}, using default")
            df.loc[0, 's_sertifikat'] = known_sertifikat[0]
        
        # Encoding
        df['kabupaten_encoded'] = self.le_kabupaten.transform(df['kabupaten'])
        df['s_sertifikat_encoded'] = self.le_sertifikat.transform(df['s_sertifikat'])
        
        # Drop original string columns
        df = df.drop(['kabupaten', 's_sertifikat'], axis=1)
        
        # Reorder columns
        df = df[self.feature_columns]
        
        # Scale data
        scaled_data = self.scaler.transform(df)
        
        return scaled_data
    
    def predict(self, preprocessed_data: np.ndarray) -> float:
        """Melakukan prediksi"""
        if not self._models_loaded:
            raise RuntimeError("Models not loaded yet")
        
        prediction = self.model.predict(preprocessed_data)
        return float(prediction[0])