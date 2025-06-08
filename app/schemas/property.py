# ================================
# app/schemas/property.py
# ================================
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class PropertySpecifications(BaseModel):
    bedrooms: int
    bathrooms: int
    land_area: str
    building_area: str
    carport_capacity: Optional[int] = None
    certificate_type: str
    electricity_power: str
    maid_bedrooms: Optional[int] = None
    maid_bathrooms: Optional[int] = None
    number_of_floors: int
    property_condition: str

class PropertyBase(BaseModel):
    title: str
    description: str
    monthly_installment_info: Optional[str] = None
    price_display: str
    price_numeric: float
    location_text: str
    estimated_savings: Optional[str] = None
    posted_by: str
    source_url: str
    property_type: str = Field(..., pattern="^(House|Apartment|Other)$")
    facilities: Optional[List[str]] = None
    specifications: PropertySpecifications
    nearby_points_of_interest: Optional[dict] = None

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    pass

class PropertyResponse(PropertyBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

# Standard API Response Models
class ApiResponse(BaseModel):
    status: str = Field(..., pattern="^(success|fail|error)$")
    data: Optional[Any] = None
    error: Optional[dict] = None

class PaginationMeta(BaseModel):
    total: int
    limit: int
    offset: int
    has_next: bool
    has_prev: bool

class PropertiesListResponse(BaseModel):
    status: str = Field(default="success")
    data: List[PropertyResponse]
    meta: PaginationMeta
    error: Optional[dict] = None

class PropertyStatsResponse(BaseModel):
    status: str = Field(default="success")
    data: dict
    error: Optional[dict] = None

class PropertyFeatures(BaseModel):
    # Fasilitas properti (0 atau 1)
    f_taman: int = Field(ge=0, le=1, description="Fasilitas taman (0/1)")
    f_jogging_track: int = Field(ge=0, le=1, description="Fasilitas jogging track (0/1)")
    f_cctv: int = Field(ge=0, le=1, description="Fasilitas CCTV (0/1)")
    f_lapangan_voli: int = Field(ge=0, le=1, description="Fasilitas lapangan voli (0/1)")
    f_lapangan_bola: int = Field(ge=0, le=1, description="Fasilitas lapangan bola (0/1)")
    f_lapangan_basket: int = Field(ge=0, le=1, description="Fasilitas lapangan basket (0/1)")
    f_lapangan_bulu_tangkis: int = Field(ge=0, le=1, description="Fasilitas lapangan bulu tangkis (0/1)")
    f_tempat_jemuran: int = Field(ge=0, le=1, description="Fasilitas tempat jemuran (0/1)")
    f_kulkas: int = Field(ge=0, le=1, description="Fasilitas kulkas (0/1)")
    f_telepon: int = Field(ge=0, le=1, description="Fasilitas telepon (0/1)")
    f_tempat_cuci: int = Field(ge=0, le=1, description="Fasilitas tempat cuci (0/1)")
    f_laundry: int = Field(ge=0, le=1, description="Fasilitas laundry (0/1)")
    f_masjid: int = Field(ge=0, le=1, description="Fasilitas masjid (0/1)")
    f_taman_bermain: int = Field(ge=0, le=1, description="Fasilitas taman bermain (0/1)")
    f_kolam_renang: int = Field(ge=0, le=1, description="Fasilitas kolam renang (0/1)")
    f_mesin_cuci: int = Field(ge=0, le=1, description="Fasilitas mesin cuci (0/1)")
    f_kompor: int = Field(ge=0, le=1, description="Fasilitas kompor (0/1)")
    f_keamanan_24_jam: int = Field(ge=0, le=1, description="Fasilitas keamanan 24 jam (0/1)")
    f_kolam_ikan: int = Field(ge=0, le=1, description="Fasilitas kolam ikan (0/1)")
    f_backyard: int = Field(ge=0, le=1, description="Fasilitas backyard (0/1)")
    f_kitchen_set: int = Field(ge=0, le=1, description="Fasilitas kitchen set (0/1)")
    f_teras: int = Field(ge=0, le=1, description="Fasilitas teras (0/1)")
    f_wastafel: int = Field(ge=0, le=1, description="Fasilitas wastafel (0/1)")
    f_akses_parkir: int = Field(ge=0, le=1, description="Fasilitas akses parkir (0/1)")
    f_lapangan_tenis: int = Field(ge=0, le=1, description="Fasilitas lapangan tenis (0/1)")
    f_tempat_gym: int = Field(ge=0, le=1, description="Fasilitas tempat gym (0/1)")
    f_ac: int = Field(ge=0, le=1, description="Fasilitas AC (0/1)")
    f_water_heater: int = Field(ge=0, le=1, description="Fasilitas water heater (0/1)")
    f_one_gate_system: int = Field(ge=0, le=1, description="Fasilitas one gate system (0/1)")
    
    # Spesifikasi properti
    s_jumlah_lantai: int = Field(ge=1, description="Jumlah lantai")
    s_kamar_mandi: int = Field(ge=1, description="Jumlah kamar mandi")
    s_kamar_tidur: int = Field(ge=1, description="Jumlah kamar tidur")
    s_luas_bangunan: float = Field(gt=0, description="Luas bangunan (m²)")
    s_luas_tanah: float = Field(gt=0, description="Luas tanah (m²)")
    
    # Point of Interest (jarak dalam km)
    poi_perbelanjaan: float = Field(ge=0, description="Jarak ke pusat perbelanjaan (km)")
    poi_sekolah: float = Field(ge=0, description="Jarak ke sekolah (km)")
    poi_transportasi: float = Field(ge=0, description="Jarak ke transportasi umum (km)")
    
    # Lokasi dan sertifikat
    kabupaten: str = Field(description="Nama kabupaten/kota")
    s_sertifikat: str = Field(description="Jenis sertifikat properti")

    class Config:
        schema_extra = {
            "example": {
                "f_taman": 1, "f_jogging_track": 0, "f_cctv": 1, "f_lapangan_voli": 0,
                "f_lapangan_bola": 0, "f_lapangan_basket": 1, "f_lapangan_bulu_tangkis": 0,
                "f_tempat_jemuran": 1, "f_kulkas": 1, "f_telepon": 0, "f_tempat_cuci": 1,
                "f_laundry": 0, "f_masjid": 1, "f_taman_bermain": 1, "f_kolam_renang": 0,
                "f_mesin_cuci": 1, "f_kompor": 1, "f_keamanan_24_jam": 1, "f_kolam_ikan": 0,
                "f_backyard": 1, "f_kitchen_set": 1, "f_teras": 1, "f_wastafel": 1,
                "f_akses_parkir": 1, "f_lapangan_tenis": 0, "f_tempat_gym": 0, "f_ac": 1,
                "f_water_heater": 1, "f_one_gate_system": 1, "s_jumlah_lantai": 2,
                "s_kamar_mandi": 2, "s_kamar_tidur": 3, "s_luas_bangunan": 120.5,
                "s_luas_tanah": 200.0, "poi_perbelanjaan": 2.5, "poi_sekolah": 1.0,
                "poi_transportasi": 0.8, "kabupaten": "Jakarta Selatan", "s_sertifikat": "SHM"
            }
        }