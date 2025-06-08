# # main.py

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import pandas as pd
# import numpy as np
# import joblib
# from huggingface_hub import hf_hub_download

# # --- Inisialisasi FastAPI ---
# app = FastAPI(title="Property Price Prediction API")

# # --- Unduh dan muat model dan pre-processing object dari Hugging Face Hub ---
# le_kabupaten_path = hf_hub_download("stevencmichael/Capstone_Project_SM079-LAI", "le_kabupaten.joblib")
# le_sertifikat_path = hf_hub_download("stevencmichael/Capstone_Project_SM079-LAI", "le_sertifikat.joblib")
# scaler_path = hf_hub_download("stevencmichael/Capstone_Project_SM079-LAI", "standard_scaler.joblib")
# model_path = hf_hub_download("stevencmichael/Capstone_Project_SM079-LAI", "model.joblib")

# loaded_le_kabupaten = joblib.load(le_kabupaten_path)
# loaded_le_sertifikat = joblib.load(le_sertifikat_path)
# loaded_scaler = joblib.load(scaler_path)
# loaded_model = joblib.load(model_path)

# # --- Daftar kolom yang dibutuhkan oleh model ---
# MODEL_FEATURES = [
#     'f_taman', 'f_jogging_track', 'f_cctv', 'f_lapangan_voli', 'f_lapangan_bola',
#     'f_lapangan_basket', 'f_lapangan_bulu_tangkis', 'f_tempat_jemuran', 'f_kulkas',
#     'f_telepon', 'f_tempat_cuci', 'f_laundry', 'f_masjid', 'f_taman_bermain',
#     'f_kolam_renang', 'f_mesin_cuci', 'f_kompor', 'f_keamanan_24_jam', 'f_kolam_ikan',
#     'f_backyard', 'f_kitchen_set', 'f_teras', 'f_wastafel', 'f_akses_parkir',
#     'f_lapangan_tenis', 'f_tempat_gym', 'f_ac', 'f_water_heater', 'f_one_gate_system',
#     's_jumlah_lantai', 's_kamar_mandi', 's_kamar_tidur', 's_luas_bangunan', 's_luas_tanah',
#     'poi_perbelanjaan', 'poi_sekolah', 'poi_transportasi',
#     'kabupaten', 's_sertifikat'
# ]

# # --- Skema data input ---
# class PropertyFeatures(BaseModel):
#     f_taman: int
#     f_jogging_track: int
#     f_cctv: int
#     f_lapangan_voli: int
#     f_lapangan_bola: int
#     f_lapangan_basket: int
#     f_lapangan_bulu_tangkis: int
#     f_tempat_jemuran: int
#     f_kulkas: int
#     f_telepon: int
#     f_tempat_cuci: int
#     f_laundry: int
#     f_masjid: int
#     f_taman_bermain: int
#     f_kolam_renang: int
#     f_mesin_cuci: int
#     f_kompor: int
#     f_keamanan_24_jam: int
#     f_kolam_ikan: int
#     f_backyard: int
#     f_kitchen_set: int
#     f_teras: int
#     f_wastafel: int
#     f_akses_parkir: int
#     f_lapangan_tenis: int
#     f_tempat_gym: int
#     f_ac: int
#     f_water_heater: int
#     f_one_gate_system: int
#     s_jumlah_lantai: int
#     s_kamar_mandi: int
#     s_kamar_tidur: int
#     s_luas_bangunan: float
#     s_luas_tanah: float
#     poi_perbelanjaan: float
#     poi_sekolah: float
#     poi_transportasi: float
#     kabupaten: str
#     s_sertifikat: str

# # --- Endpoint prediksi ---
# @app.post("/predict")
# def predict_price(features: PropertyFeatures):
#     try:
#         # Konversi input JSON ke DataFrame
#         input_data = pd.DataFrame([features.dict()])

#         # Pre-processing
#         # Lowercase dan strip untuk kolom string
#         input_data['kabupaten'] = input_data['kabupaten'].str.lower().str.strip()
#         input_data['s_sertifikat'] = input_data['s_sertifikat'].str.lower().str.strip()

#         # Handle kabupaten tidak dikenal
#         known_kabupaten = loaded_le_kabupaten.classes_
#         if not input_data.loc[0, 'kabupaten'] in known_kabupaten:
#             input_data.loc[0, 'kabupaten'] = known_kabupaten[0]

#         # Handle s_sertifikat tidak dikenal
#         known_sertifikat = loaded_le_sertifikat.classes_
#         if not input_data.loc[0, 's_sertifikat'] in known_sertifikat:
#             input_data.loc[0, 's_sertifikat'] = known_sertifikat[0]

#         # Encoding
#         input_data['kabupaten_encoded'] = loaded_le_kabupaten.transform(input_data['kabupaten'])
#         input_data['s_sertifikat_encoded'] = loaded_le_sertifikat.transform(input_data['s_sertifikat'])

#         # Hapus kolom asli string
#         input_data = input_data.drop(['kabupaten', 's_sertifikat'], axis=1)

#         # Urutkan kolom sesuai model
#         final_features = [
#             'f_taman', 'f_jogging_track', 'f_cctv', 'f_lapangan_voli', 'f_lapangan_bola',
#             'f_lapangan_basket', 'f_lapangan_bulu_tangkis', 'f_tempat_jemuran', 'f_kulkas',
#             'f_telepon', 'f_tempat_cuci', 'f_laundry', 'f_masjid', 'f_taman_bermain',
#             'f_kolam_renang', 'f_mesin_cuci', 'f_kompor', 'f_keamanan_24_jam', 'f_kolam_ikan',
#             'f_backyard', 'f_kitchen_set', 'f_teras', 'f_wastafel', 'f_akses_parkir',
#             'f_lapangan_tenis', 'f_tempat_gym', 'f_ac', 'f_water_heater', 'f_one_gate_system',
#             's_jumlah_lantai', 's_kamar_mandi', 's_kamar_tidur', 's_luas_bangunan', 's_luas_tanah',
#             'poi_perbelanjaan', 'poi_sekolah', 'poi_transportasi',
#             'kabupaten_encoded', 's_sertifikat_encoded'
#         ]
#         input_data = input_data[final_features]

#         # Scaling
#         scaled_data = loaded_scaler.transform(input_data)

#         # Prediksi
#         prediction = loaded_model.predict(scaled_data)

#         return {
#             "prediksi_harga": float(prediction[0]),
#             "status": "success"
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

# # --- Endpoint Root ---
# @app.get("/")
# def read_root():
#     return {"message": "Property Price Prediction API. Use POST /predict with JSON data."}
