# Property Management API

Simple CRUD API untuk manajemen properti menggunakan FastAPI dan PostgreSQL.

## Features

- ✅ CRUD Operations untuk properti
- ✅ Filtering dan sorting
- ✅ Pagination
- ✅ Statistics endpoint
- ✅ Health check
- ✅ CORS support
- ✅ Pydantic validation
- ✅ SQLAlchemy ORM

## Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Project Structure

```
property-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point aplikasi
│   ├── database.py             # Konfigurasi database
│   ├── models/
│   │   ├── __init__.py
│   │   └── property.py         # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── property.py         # Pydantic models
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencies
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── properties.py   # Property endpoints
│   │       └── health.py       # Health check
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Konfigurasi
│   └── utils/
│       ├── __init__.py
│       └── responses.py        # Helper functions
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation

1. Clone repository:

```bash
git clone <repository-url>
cd property-management-api
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Setup environment variables:

```bash
cp .env.example .env
# Edit .env file dengan konfigurasi database Anda
```

5. Run aplikasi:

```bash
python -m uvicorn app.main:app --reload
```

Aplikasi akan berjalan di `http://localhost:8000`

## API Documentation

Setelah aplikasi berjalan, akses dokumentasi API di:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Properties

- `GET /properties` - List properties dengan filtering
- `GET /properties/{id}` - Get property by ID
- `POST /properties` - Create new property
- `PUT /properties/{id}` - Update property
- `DELETE /properties/{id}` - Delete property
- `GET /properties/stats/summary` - Get statistics

### Health Check

- `GET /health` - Health check endpoint

## Query Parameters untuk GET /properties

- `location_text` - Filter berdasarkan lokasi
- `property_type` - Filter berdasarkan tipe (House|Apartment|Other)
- `bedrooms` - Filter berdasarkan jumlah kamar tidur
- `bathrooms` - Filter berdasarkan jumlah kamar mandi
- `min_price` - Harga minimum
- `max_price` - Harga maksimum
- `sort` - Sorting berdasarkan harga (asc|desc)
- `limit` - Jumlah data per halaman (default: 10)
- `offset` - Starting index untuk pagination (default: 0)

## Response Format

### Success Response

```json
{
  "status": "success",
  "data": { ... },
  "error": null
}
```

### Error Response

```json
{
  "status": "error",
  "data": null,
  "error": {
    "code": 404,
    "message": "Property not found"
  }
}
```

## Development

### Menjalankan dengan auto-reload:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing API dengan curl:

```bash
# Get all properties
curl http://localhost:8000/properties

# Get property by ID
curl http://localhost:8000/properties/1

# Health check
curl http://localhost:8000/health
```

## Environment Variables

Buat file `.env` di root project:

```env
DATABASE_URL=postgresql://username:password@host:port/database
PROJECT_NAME=Property Management API
PROJECT_VERSION=1.0.0
```

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push branch: `git push origin feature/new-feature`
5. Submit Pull Request
