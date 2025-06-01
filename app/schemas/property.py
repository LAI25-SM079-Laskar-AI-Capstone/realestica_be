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
