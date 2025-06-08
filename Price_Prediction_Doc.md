# 🏠 Realestica Real Estate Price Prediction API Documentation

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Request Schema](#request-schema)
- [Response Schema](#response-schema)
- [Example Requests](#example-requests)
- [Error Handling](#error-handling)
- [Model Information](#model-information)
- [Performance Notes](#performance-notes)
- [Best Practices](#best-practices)

---

## 🎯 Overview

Realestica Real Estate Price Prediction API menggunakan machine learning untuk memprediksi harga properti berdasarkan berbagai fitur seperti fasilitas, spesifikasi, lokasi, dan point of interest. API ini dibangun dengan FastAPI dan menggunakan model yang telah dilatih dari dataset properti Indonesia.

### Key Features

- ⚡ **Fast Prediction**: Model dimuat saat startup untuk performa optimal
- 🎯 **Accurate**: Menggunakan 39 fitur untuk prediksi yang akurat
- 🔒 **Validated Input**: Validasi input menggunakan Pydantic
- 📊 **Comprehensive**: Mencakup fasilitas, spesifikasi, dan lokasi
- 🌍 **Location-aware**: Mendukung berbagai kabupaten/kota di Jakarta [Barat, Timur, Selatan, Utara, Pusat]

---

## 🚀 Quick Start

### Base URL

```
http://localhost:8000
```

### Authentication

Tidak diperlukan authentication untuk endpoint prediksi.

### Content-Type

```
Content-Type: application/json
```

---

## 🔗 API Endpoints

### 1. Predict Property Price

**Endpoint**: `POST /predict/`

Memprediksi harga properti berdasarkan fitur-fitur yang diberikan.

**Parameters**: Body (JSON) - PropertyFeatures object

**Response**: JSON dengan prediksi harga dan status

### 2. Get Model Information

**Endpoint**: `GET /predict/model-info`

Mendapatkan informasi tentang model ML yang digunakan.

**Parameters**: None

**Response**: JSON dengan informasi model

---

## 📝 Request Schema

### PropertyFeatures Object

#### 🏢 Fasilitas Properti (0 atau 1)

| Field                     | Type    | Description                     | Required |
| ------------------------- | ------- | ------------------------------- | -------- |
| `f_taman`                 | integer | Fasilitas taman                 | ✅       |
| `f_jogging_track`         | integer | Fasilitas jogging track         | ✅       |
| `f_cctv`                  | integer | Fasilitas CCTV                  | ✅       |
| `f_lapangan_voli`         | integer | Fasilitas lapangan voli         | ✅       |
| `f_lapangan_bola`         | integer | Fasilitas lapangan bola         | ✅       |
| `f_lapangan_basket`       | integer | Fasilitas lapangan basket       | ✅       |
| `f_lapangan_bulu_tangkis` | integer | Fasilitas lapangan bulu tangkis | ✅       |
| `f_tempat_jemuran`        | integer | Fasilitas tempat jemuran        | ✅       |
| `f_kulkas`                | integer | Fasilitas kulkas                | ✅       |
| `f_telepon`               | integer | Fasilitas telepon               | ✅       |
| `f_tempat_cuci`           | integer | Fasilitas tempat cuci           | ✅       |
| `f_laundry`               | integer | Fasilitas laundry               | ✅       |
| `f_masjid`                | integer | Fasilitas masjid                | ✅       |
| `f_taman_bermain`         | integer | Fasilitas taman bermain         | ✅       |
| `f_kolam_renang`          | integer | Fasilitas kolam renang          | ✅       |
| `f_mesin_cuci`            | integer | Fasilitas mesin cuci            | ✅       |
| `f_kompor`                | integer | Fasilitas kompor                | ✅       |
| `f_keamanan_24_jam`       | integer | Fasilitas keamanan 24 jam       | ✅       |
| `f_kolam_ikan`            | integer | Fasilitas kolam ikan            | ✅       |
| `f_backyard`              | integer | Fasilitas backyard              | ✅       |
| `f_kitchen_set`           | integer | Fasilitas kitchen set           | ✅       |
| `f_teras`                 | integer | Fasilitas teras                 | ✅       |
| `f_wastafel`              | integer | Fasilitas wastafel              | ✅       |
| `f_akses_parkir`          | integer | Fasilitas akses parkir          | ✅       |
| `f_lapangan_tenis`        | integer | Fasilitas lapangan tenis        | ✅       |
| `f_tempat_gym`            | integer | Fasilitas tempat gym            | ✅       |
| `f_ac`                    | integer | Fasilitas AC                    | ✅       |
| `f_water_heater`          | integer | Fasilitas water heater          | ✅       |
| `f_one_gate_system`       | integer | Fasilitas one gate system       | ✅       |

#### 🏗️ Spesifikasi Properti

| Field             | Type    | Description        | Range | Required |
| ----------------- | ------- | ------------------ | ----- | -------- |
| `s_jumlah_lantai` | integer | Jumlah lantai      | ≥ 1   | ✅       |
| `s_kamar_mandi`   | integer | Jumlah kamar mandi | ≥ 1   | ✅       |
| `s_kamar_tidur`   | integer | Jumlah kamar tidur | ≥ 1   | ✅       |
| `s_luas_bangunan` | float   | Luas bangunan (m²) | > 0   | ✅       |
| `s_luas_tanah`    | float   | Luas tanah (m²)    | > 0   | ✅       |

#### 📍 Point of Interest (Jarak dalam km)

| Field              | Type  | Description                 | Range | Required |
| ------------------ | ----- | --------------------------- | ----- | -------- |
| `poi_perbelanjaan` | float | Jarak ke pusat perbelanjaan | ≥ 0   | ✅       |
| `poi_sekolah`      | float | Jarak ke sekolah            | ≥ 0   | ✅       |
| `poi_transportasi` | float | Jarak ke transportasi umum  | ≥ 0   | ✅       |

#### 🌍 Lokasi dan Sertifikat

| Field          | Type   | Description               | Required |
| -------------- | ------ | ------------------------- | -------- |
| `kabupaten`    | string | Nama kabupaten/kota       | ✅       |
| `s_sertifikat` | string | Jenis sertifikat properti | ✅       |

---

## 📤 Response Schema

### Successful Prediction Response

```json
{
  "status": "success",
  "data": {
    "prediksi_harga": 1250000000.0,
    "prediksi_harga_formatted": "Rp 1.25 Miliar",
    "status": "success"
  },
  "timestamp": "2025-06-08T10:30:00Z"
}
```

### Model Info Response

```json
{
  "status": "success",
  "data": {
    "model_loaded": true,
    "available_kabupaten": ["jakarta selatan", "jakarta pusat", "bandung", ...],
    "available_sertifikat": ["shm", "hgb", "hgu", ...],
    "total_features": 39,
    "model_source": "stevencmichael/Capstone_Project_SM079-LAI"
  },
  "timestamp": "2025-06-08T10:30:00Z"
}
```

### Error Response

```json
{
  "status": "error",
  "error": "Error during prediction: ...",
  "timestamp": "2025-06-08T10:30:00Z"
}
```

---

## 💡 Example Requests

### 1. Rumah Mewah Jakarta Selatan

```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "f_taman": 1,
    "f_jogging_track": 1,
    "f_cctv": 1,
    "f_lapangan_voli": 0,
    "f_lapangan_bola": 1,
    "f_lapangan_basket": 1,
    "f_lapangan_bulu_tangkis": 1,
    "f_tempat_jemuran": 1,
    "f_kulkas": 1,
    "f_telepon": 1,
    "f_tempat_cuci": 1,
    "f_laundry": 1,
    "f_masjid": 1,
    "f_taman_bermain": 1,
    "f_kolam_renang": 1,
    "f_mesin_cuci": 1,
    "f_kompor": 1,
    "f_keamanan_24_jam": 1,
    "f_kolam_ikan": 1,
    "f_backyard": 1,
    "f_kitchen_set": 1,
    "f_teras": 1,
    "f_wastafel": 1,
    "f_akses_parkir": 1,
    "f_lapangan_tenis": 1,
    "f_tempat_gym": 1,
    "f_ac": 1,
    "f_water_heater": 1,
    "f_one_gate_system": 1,
    "s_jumlah_lantai": 3,
    "s_kamar_mandi": 4,
    "s_kamar_tidur": 5,
    "s_luas_bangunan": 350.0,
    "s_luas_tanah": 500.0,
    "poi_perbelanjaan": 1.2,
    "poi_sekolah": 0.8,
    "poi_transportasi": 0.5,
    "kabupaten": "Jakarta Selatan",
    "s_sertifikat": "SHM"
  }'
```

**Response:**

```json
{
  "success": true,
  "data": {
    "prediksi_harga": 4750000000.0,
    "prediksi_harga_formatted": "Rp 4.75 Miliar",
    "status": "success"
  },
  "timestamp": "2025-06-08T10:30:00Z"
}
```

### 2. Rumah Sederhana Jakarta Timur

```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "f_taman": 0,
    "f_jogging_track": 0,
    "f_cctv": 1,
    "f_lapangan_voli": 0,
    "f_lapangan_bola": 0,
    "f_lapangan_basket": 0,
    "f_lapangan_bulu_tangkis": 0,
    "f_tempat_jemuran": 1,
    "f_kulkas": 1,
    "f_telepon": 0,
    "f_tempat_cuci": 1,
    "f_laundry": 0,
    "f_masjid": 1,
    "f_taman_bermain": 0,
    "f_kolam_renang": 0,
    "f_mesin_cuci": 0,
    "f_kompor": 1,
    "f_keamanan_24_jam": 1,
    "f_kolam_ikan": 0,
    "f_backyard": 0,
    "f_kitchen_set": 1,
    "f_teras": 1,
    "f_wastafel": 1,
    "f_akses_parkir": 1,
    "f_lapangan_tenis": 0,
    "f_tempat_gym": 0,
    "f_ac": 0,
    "f_water_heater": 0,
    "f_one_gate_system": 0,
    "s_jumlah_lantai": 1,
    "s_kamar_mandi": 1,
    "s_kamar_tidur": 2,
    "s_luas_bangunan": 60.0,
    "s_luas_tanah": 90.0,
    "poi_perbelanjaan": 3.5,
    "poi_sekolah": 2.0,
    "poi_transportasi": 1.5,
    "kabupaten": "Jakarta Timur",
    "s_sertifikat": "SHM"
  }'
```

**Response:**

```json
{
  "success": true,
  "data": {
    "prediksi_harga": 450000000.0,
    "prediksi_harga_formatted": "Rp 450.00 Juta",
    "status": "success"
  },
  "timestamp": "2025-06-08T10:30:00Z"
}
```

### 3. Apartemen Jakarta Pusat

```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "f_taman": 1,
    "f_jogging_track": 1,
    "f_cctv": 1,
    "f_lapangan_voli": 1,
    "f_lapangan_bola": 0,
    "f_lapangan_basket": 1,
    "f_lapangan_bulu_tangkis": 1,
    "f_tempat_jemuran": 1,
    "f_kulkas": 1,
    "f_telepon": 1,
    "f_tempat_cuci": 1,
    "f_laundry": 1,
    "f_masjid": 1,
    "f_taman_bermain": 1,
    "f_kolam_renang": 1,
    "f_mesin_cuci": 1,
    "f_kompor": 1,
    "f_keamanan_24_jam": 1,
    "f_kolam_ikan": 0,
    "f_backyard": 0,
    "f_kitchen_set": 1,
    "f_teras": 1,
    "f_wastafel": 1,
    "f_akses_parkir": 1,
    "f_lapangan_tenis": 0,
    "f_tempat_gym": 1,
    "f_ac": 1,
    "f_water_heater": 1,
    "f_one_gate_system": 1,
    "s_jumlah_lantai": 1,
    "s_kamar_mandi": 2,
    "s_kamar_tidur": 2,
    "s_luas_bangunan": 80.0,
    "s_luas_tanah": 90.0,
    "poi_perbelanjaan": 0.5,
    "poi_sekolah": 1.2,
    "poi_transportasi": 0.3,
    "kabupaten": "Jakarta Pusat",
    "s_sertifikat": "SHM"
  }'
```

**Response:**

```json
{
  "success": true,
  "data": {
    "prediksi_harga": 1850000000.0,
    "prediksi_harga_formatted": "Rp 1.85 Miliar",
    "status": "success"
  },
  "timestamp": "2025-06-08T10:30:00Z"
}
```

### 4. Get Model Information

```bash
curl -X GET "http://localhost:8000/predict/model-info"
```

**Response:**

```json
{
  "success": true,
  "data": {
    "model_loaded": true,
    "available_kabupaten": ["jakarta selatan", "jakarta pusat", "jakarta barat", "jakarta utara", "jakarta timur", "bandung", "bekasi", "tangerang", "depok", "bogor"],
    "available_sertifikat": ["shm", "hgb", "hgu", "shgb", "girik"],
    "total_features": 39,
    "model_source": "stevencmichael/Capstone_Project_SM079-LAI"
  },
  "timestamp": "2025-06-08T10:30:00Z"
}
```

---

## 🚨 Error Handling

### Common Errors

#### 1. Validation Error (422)

```json
{
  "detail": [
    {
      "loc": ["body", "s_luas_bangunan"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt",
      "ctx": { "limit_value": 0 }
    }
  ]
}
```

#### 2. Model Not Loaded (503)

```json
{
  "success": false,
  "error": "ML models not loaded yet",
  "timestamp": "2025-06-08T10:30:00Z"
}
```

#### 3. Prediction Error (500)

```json
{
  "success": false,
  "error": "Error during prediction: Invalid input data format",
  "timestamp": "2025-06-08T10:30:00Z"
}
```

### Error Codes

| Status Code | Description                            |
| ----------- | -------------------------------------- |
| 200         | Success                                |
| 422         | Validation Error                       |
| 500         | Internal Server Error                  |
| 503         | Service Unavailable (Model not loaded) |

---

## 🤖 Model Information

### Model Details

- **Model Type**: Ensemble Machine Learning Model
- **Features**: 39 input features
- **Training Data**: Indonesian real estate dataset
- **Accuracy**: Optimized for Indonesian property market

### Supported Locations

Model mendukung prediksi untuk berbagai kabupaten/kota di Indonesia. Untuk mendapatkan daftar lengkap, gunakan endpoint `/predict/model-info`.

**Contoh kabupaten yang didukung:**

- Jakarta Selatan, Jakarta Pusat, Jakarta Barat, Jakarta Utara, Jakarta Timur
- Bandung, Bekasi, Tangerang, Depok, Bogor
- Dan banyak lagi...

### Supported Certificate Types

- **SHM** (Sertifikat Hak Milik)
- **HGB** (Hak Guna Bangunan)
- **HGU** (Hak Guna Usaha)
- **SHGB** (Sertifikat Hak Guna Bangunan)
- **Girik** (Surat Girik)

---

## ⚡ Performance Notes

### Response Times

- **Cold Start**: ~2-3 seconds (hanya saat startup)
- **Warm Requests**: ~50-200ms
- **Model Loading**: Dilakukan saat startup aplikasi

### Optimizations

- Model dimuat saat startup untuk performa optimal
- Singleton pattern mencegah loading berulang
- Preprocessing pipeline yang efisien
- Caching untuk response yang konsisten

### Rate Limiting

Tidak ada rate limiting default, namun disarankan untuk implementasi production:

- **Recommended**: 100 requests/minute per IP
- **Burst**: 20 requests/second

---

## 🎯 Best Practices

### 1. Input Validation

- Pastikan semua field required terisi
- Gunakan nilai 0 atau 1 untuk fasilitas
- Validasi range untuk field numerik

### 2. Error Handling

```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/predict/",
        json=property_data,
        timeout=10
    )
    response.raise_for_status()
    result = response.json()

    if result.get("success"):
        price = result["data"]["prediksi_harga"]
        formatted_price = result["data"]["prediksi_harga_formatted"]
    else:
        print(f"Prediction failed: {result.get('error')}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### 3. Batch Processing

Untuk prediksi multiple properties, gunakan loop dengan delay:

```python
import time

properties = [property1, property2, property3]
results = []

for prop in properties:
    response = requests.post(url, json=prop)
    results.append(response.json())
    time.sleep(0.1)  # Avoid overwhelming the server
```

### 4. Caching

Implementasikan caching untuk properties yang sama:

```python
import hashlib
import json

def get_property_hash(property_data):
    return hashlib.md5(
        json.dumps(property_data, sort_keys=True).encode()
    ).hexdigest()

# Cache results for identical properties
cache = {}
prop_hash = get_property_hash(property_data)

if prop_hash in cache:
    result = cache[prop_hash]
else:
    result = requests.post(url, json=property_data).json()
    cache[prop_hash] = result
```

### 5. Production Deployment

- Gunakan HTTPS untuk production
- Implementasikan rate limiting
- Monitor response times dan error rates
- Setup logging untuk debugging
- Gunakan load balancer untuk high availability

---

## 📊 Usage Analytics

### Tracking Recommendations

```python
# Log prediction requests
logging.info(f"Prediction request: {kabupaten}, {s_luas_bangunan}m², Price: {predicted_price}")

# Track popular locations
location_stats = {
    "jakarta_selatan": 1234,
    "bandung": 567,
    "jakarta_pusat": 890
}

# Monitor prediction accuracy
# Compare with actual market prices when available
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Model Not Loading

**Problem**: "ML models not loaded yet" error
**Solution**:

- Check Hugging Face Hub connectivity
- Verify model files are accessible
- Restart the application

#### 2. Slow Predictions

**Problem**: Predictions taking too long
**Solution**:

- Ensure model is loaded at startup
- Check server resources (CPU, Memory)
- Optimize input data preprocessing

#### 3. Validation Errors

**Problem**: Field validation failing
**Solution**:

- Check field types and ranges
- Ensure all required fields are provided
- Validate against schema documentation

#### 4. Unknown Location/Certificate

**Problem**: Unsupported kabupaten or certificate type
**Solution**:

- Check available options via `/predict/model-info`
- Use closest available location
- Contact support for new location support

---

## 📞 Support & Contact

### API Support

- **Documentation**: `/docs` (Swagger UI)
- **Health Check**: `/health`
- **Model Status**: `/predict/model-info`

### Getting Help

1. Check this documentation first
2. Verify input data format
3. Test with provided examples
4. Check server logs for detailed errors

---

## 📈 Changelog

### Version 1.0.0

- Initial release
- 39 feature prediction model
- Support for major Indonesian cities
- Optimized startup and prediction performance

---

_Dokumentasi ini akan terus diperbarui seiring dengan pengembangan API. Untuk informasi terbaru, silakan periksa endpoint `/docs` atau hubungi tim development._
