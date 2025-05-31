# main.py
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime
import json

# Database Configuration
password = "CbM8qZp3W3K1zYpm"
database_url = f"postgresql://postgres.wodlrtysmleajqytwbnu:{password}@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI App
app = FastAPI(
    title="Property Management API",
    description="Simple CRUD API for Property Management",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Models
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
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic Models
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
    
    # Specifications as separate fields
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
    
    nearby_points_of_interest_text: Optional[str] = None

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

class PropertiesListResponse(BaseModel):
    data: List[PropertyResponse]
    total: int
    limit: int
    offset: int
    has_next: bool
    has_prev: bool

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)

# Helper function to convert SQLAlchemy model to Pydantic
def property_to_response(property_model: PropertyModel) -> PropertyResponse:
    # Handle facilities field - convert string to list if needed
    facilities = []
    if property_model.facilities:
        if isinstance(property_model.facilities, list):
            facilities = property_model.facilities
        elif isinstance(property_model.facilities, str):
            # If it's a string, split by comma or treat as single item
            facilities = [facility.strip() for facility in property_model.facilities.split(',') if facility.strip()]
            if not facilities:  # If splitting didn't work, treat as single item
                facilities = [property_model.facilities]
    
    return PropertyResponse(
        id=property_model.id,
        title=property_model.title,
        description=property_model.description,
        monthly_installment_info=property_model.monthly_installment_info,
        price_display=property_model.price_display,
        price_numeric=property_model.price_numeric,
        location_text=property_model.location_text,
        estimated_savings=property_model.estimated_savings,
        posted_by=property_model.posted_by,
        source_url=property_model.source_url,
        property_type=property_model.property_type,
        facilities=facilities,
        bedrooms=property_model.bedrooms,
        bathrooms=property_model.bathrooms,
        land_area=property_model.land_area,
        building_area=property_model.building_area,
        carport_capacity=property_model.carport_capacity,
        certificate_type=property_model.certificate_type,
        electricity_power=property_model.electricity_power,
        maid_bedrooms=property_model.maid_bedrooms,
        maid_bathrooms=property_model.maid_bathrooms,
        number_of_floors=property_model.number_of_floors,
        property_condition=property_model.property_condition,
        nearby_points_of_interest_text=property_model.nearby_points_of_interest_text,
        createdAt=property_model.createdAt,
        updatedAt=property_model.updatedAt
    )

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Property Management API", "version": "1.0.0"}

@app.get("/properties", response_model=PropertiesListResponse, tags=["Properties"])
async def get_properties(
    location_text: Optional[str] = Query(None, description="Filter by location"),
    property_type: Optional[str] = Query(None, pattern="^(House|Apartment|Other)$", description="Filter by property type"),
    bedrooms: Optional[int] = Query(None, ge=1, description="Filter by number of bedrooms"),
    bathrooms: Optional[int] = Query(None, ge=1, description="Filter by number of bathrooms"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    sort: Optional[str] = Query("desc", pattern="^(asc|desc)$", description="Sort by price (asc/desc)"),
    limit: int = Query(10, ge=1, le=100, description="Number of properties per page"),
    offset: int = Query(0, ge=0, description="Starting index for pagination"),
    db: Session = Depends(get_db)
):
    """Get list of properties with filtering, sorting, and pagination"""
    
    query = db.query(PropertyModel)
    
    # Apply filters
    if location_text:
        query = query.filter(PropertyModel.location_text.ilike(f"%{location_text}%"))
    
    if property_type:
        query = query.filter(PropertyModel.property_type == property_type)
    
    if bedrooms:
        query = query.filter(PropertyModel.bedrooms == bedrooms)
    
    if bathrooms:
        query = query.filter(PropertyModel.bathrooms == bathrooms)
    
    if min_price:
        query = query.filter(PropertyModel.price_numeric >= min_price)
    
    if max_price:
        query = query.filter(PropertyModel.price_numeric <= max_price)
    
    # Apply sorting
    if sort == "asc":
        query = query.order_by(PropertyModel.price_numeric.asc())
    else:
        query = query.order_by(PropertyModel.price_numeric.desc())
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    properties = query.offset(offset).limit(limit).all()
    
    # Convert to response format
    property_responses = [property_to_response(prop) for prop in properties]
    
    return PropertiesListResponse(
        data=property_responses,
        total=total,
        limit=limit,
        offset=offset,
        has_next=offset + limit < total,
        has_prev=offset > 0
    )

@app.get("/properties/{property_id}", response_model=PropertyResponse, tags=["Properties"])
async def get_property(property_id: int, db: Session = Depends(get_db)):
    """Get a specific property by ID"""
    
    property_model = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
    
    if not property_model:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return property_to_response(property_model)

@app.post("/properties", response_model=PropertyResponse, tags=["Properties"], status_code=201)
async def create_property(property_data: PropertyCreate, db: Session = Depends(get_db)):
    """Create a new property"""
    
    # Convert Pydantic model to SQLAlchemy model
    property_model = PropertyModel(
        title=property_data.title,
        description=property_data.description,
        monthly_installment_info=property_data.monthly_installment_info,
        price_display=property_data.price_display,
        price_numeric=property_data.price_numeric,
        location_text=property_data.location_text,
        estimated_savings=property_data.estimated_savings,
        posted_by=property_data.posted_by,
        source_url=property_data.source_url,
        property_type=property_data.property_type,
        facilities=property_data.facilities,
        bedrooms=property_data.bedrooms,
        bathrooms=property_data.bathrooms,
        land_area=property_data.land_area,
        building_area=property_data.building_area,
        carport_capacity=property_data.carport_capacity,
        certificate_type=property_data.certificate_type,
        electricity_power=property_data.electricity_power,
        maid_bedrooms=property_data.maid_bedrooms,
        maid_bathrooms=property_data.maid_bathrooms,
        number_of_floors=property_data.number_of_floors,
        property_condition=property_data.property_condition,
        nearby_points_of_interest_text=property_data.nearby_points_of_interest_text
    )
    
    db.add(property_model)
    db.commit()
    db.refresh(property_model)
    
    return property_to_response(property_model)

@app.put("/properties/{property_id}", response_model=PropertyResponse, tags=["Properties"])
async def update_property(property_id: int, property_data: PropertyUpdate, db: Session = Depends(get_db)):
    """Update an existing property"""
    
    property_model = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
    
    if not property_model:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Update fields
    property_model.title = property_data.title
    property_model.description = property_data.description
    property_model.monthly_installment_info = property_data.monthly_installment_info
    property_model.price_display = property_data.price_display
    property_model.price_numeric = property_data.price_numeric
    property_model.location_text = property_data.location_text
    property_model.estimated_savings = property_data.estimated_savings
    property_model.posted_by = property_data.posted_by
    property_model.source_url = property_data.source_url
    property_model.property_type = property_data.property_type
    property_model.facilities = property_data.facilities
    property_model.bedrooms = property_data.bedrooms
    property_model.bathrooms = property_data.bathrooms
    property_model.land_area = property_data.land_area
    property_model.building_area = property_data.building_area
    property_model.carport_capacity = property_data.carport_capacity
    property_model.certificate_type = property_data.certificate_type
    property_model.electricity_power = property_data.electricity_power
    property_model.maid_bedrooms = property_data.maid_bedrooms
    property_model.maid_bathrooms = property_data.maid_bathrooms
    property_model.number_of_floors = property_data.number_of_floors
    property_model.property_condition = property_data.property_condition
    property_model.nearby_points_of_interest_text = property_data.nearby_points_of_interest_text
    property_model.updatedAt = datetime.utcnow()
    
    db.commit()
    db.refresh(property_model)
    
    return property_to_response(property_model)

@app.delete("/properties/{property_id}", tags=["Properties"])
async def delete_property(property_id: int, db: Session = Depends(get_db)):
    """Delete a property"""
    
    property_model = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
    
    if not property_model:
        raise HTTPException(status_code=404, detail="Property not found")
    
    db.delete(property_model)
    db.commit()
    
    return {"message": "Property deleted successfully"}

# Additional endpoint for property statistics
@app.get("/properties/stats/summary", tags=["Properties"])
async def get_property_stats(db: Session = Depends(get_db)):
    """Get property statistics summary"""
    
    total_properties = db.query(PropertyModel).count()
    
    # Count by property type
    property_type_stats = db.query(
        PropertyModel.property_type,
        func.count(PropertyModel.id).label('count')
    ).group_by(PropertyModel.property_type).all()
    
    # Average price
    avg_price = db.query(func.avg(PropertyModel.price_numeric)).scalar()
    
    # Price range
    min_price = db.query(func.min(PropertyModel.price_numeric)).scalar()
    max_price = db.query(func.max(PropertyModel.price_numeric)).scalar()
    
    return {
        "total_properties": total_properties,
        "property_types": [{"type": stat[0], "count": stat[1]} for stat in property_type_stats],
        "average_price": avg_price,
        "price_range": {
            "min": min_price,
            "max": max_price
        }
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
