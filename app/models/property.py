# ================================
# app/models/property.py
# ================================
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text
from datetime import datetime
from app.database import Base

class PropertyModel(Base):
    __tablename__ = "property"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    monthly_installment_info = Column(String, nullable=True)
    price_display = Column(String, nullable=False)
    price_numeric = Column(Float, nullable=False)
    location_text = Column(String, nullable=False)
    estimated_savings = Column(String, nullable=True)
    posted_by = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    property_type = Column(String, nullable=False)
    facilities = Column(JSON, nullable=True)
    
    # Specifications as separate columns
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    land_area = Column(String, nullable=False)
    building_area = Column(String, nullable=False)
    carport_capacity = Column(Integer, nullable=True)
    certificate_type = Column(String, nullable=False)
    electricity_power = Column(String, nullable=False)
    maid_bedrooms = Column(Integer, nullable=True)
    maid_bathrooms = Column(Integer, nullable=True)
    number_of_floors = Column(Integer, nullable=False)
    property_condition = Column(String, nullable=False)
    
    nearby_points_of_interest_text = Column(Text, nullable=True)
    createdAt = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    updatedAt = Column(DateTime, default=datetime.now(datetime.timezone.utc), onupdate=datetime.utcnow)