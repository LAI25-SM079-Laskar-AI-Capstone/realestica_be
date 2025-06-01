# ================================
# app/api/routes/properties.py
# ================================
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime

from app.models.property import PropertyModel
from app.schemas.property import (
    PropertyCreate, PropertyUpdate, PropertyResponse,
    PropertiesListResponse, PropertyStatsResponse, PaginationMeta
)
from app.api.deps import get_db
from app.utils.responses import create_error_response, create_success_response, property_to_response

router = APIRouter()

@router.get("/", response_model=PropertiesListResponse)
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
    
    try:
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
        
        meta = PaginationMeta(
            total=total,
            limit=limit,
            offset=offset,
            has_next=offset + limit < total,
            has_prev=offset > 0
        )
        
        return PropertiesListResponse(
            status="success",
            data=property_responses,
            meta=meta,
            error=None
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=create_error_response(500, "Internal server error", {"exception": str(e)})
        )

@router.get("/{property_id}")
async def get_property(property_id: int, db: Session = Depends(get_db)):
    """Get a specific property by ID"""
    
    try:
        property_model = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
        
        if not property_model:
            raise HTTPException(
                status_code=404,
                detail=create_error_response(404, "Property not found")
            )
        
        return create_success_response(property_to_response(property_model))
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=create_error_response(500, "Internal server error", {"exception": str(e)})
        )

@router.post("/", status_code=201)
async def create_property(property_data: PropertyCreate, db: Session = Depends(get_db)):
    """Create a new property"""
    
    try:
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
            bedrooms=property_data.specifications.bedrooms,
            bathrooms=property_data.specifications.bathrooms,
            land_area=property_data.specifications.land_area,
            building_area=property_data.specifications.building_area,
            carport_capacity=property_data.specifications.carport_capacity,
            certificate_type=property_data.specifications.certificate_type,
            electricity_power=property_data.specifications.electricity_power,
            maid_bedrooms=property_data.specifications.maid_bedrooms,
            maid_bathrooms=property_data.specifications.maid_bathrooms,
            number_of_floors=property_data.specifications.number_of_floors,
            property_condition=property_data.specifications.property_condition,
            nearby_points_of_interest_text=getattr(property_data, 'nearby_points_of_interest_text', None)
        )
        
        db.add(property_model)
        db.commit()
        db.refresh(property_model)
        
        return create_success_response(property_to_response(property_model))
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=create_error_response(500, "Failed to create property", {"exception": str(e)})
        )

@router.put("/{property_id}")
async def update_property(property_id: int, property_data: PropertyUpdate, db: Session = Depends(get_db)):
    """Update an existing property"""
    
    try:
        property_model = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
        
        if not property_model:
            raise HTTPException(
                status_code=404,
                detail=create_error_response(404, "Property not found")
            )
        
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
        property_model.bedrooms = property_data.specifications.bedrooms
        property_model.bathrooms = property_data.specifications.bathrooms
        property_model.land_area = property_data.specifications.land_area
        property_model.building_area = property_data.specifications.building_area
        property_model.carport_capacity = property_data.specifications.carport_capacity
        property_model.certificate_type = property_data.specifications.certificate_type
        property_model.electricity_power = property_data.specifications.electricity_power
        property_model.maid_bedrooms = property_data.specifications.maid_bedrooms
        property_model.maid_bathrooms = property_data.specifications.maid_bathrooms
        property_model.number_of_floors = property_data.specifications.number_of_floors
        property_model.property_condition = property_data.specifications.property_condition
        property_model.nearby_points_of_interest_text = getattr(property_data, 'nearby_points_of_interest_text', None)
        property_model.updatedAt = datetime.utcnow()
        
        db.commit()
        db.refresh(property_model)
        
        return create_success_response(property_to_response(property_model))
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=create_error_response(500, "Failed to update property", {"exception": str(e)})
        )

@router.delete("/{property_id}")
async def delete_property(property_id: int, db: Session = Depends(get_db)):
    """Delete a property"""
    
    try:
        property_model = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
        
        if not property_model:
            raise HTTPException(
                status_code=404,
                detail=create_error_response(404, "Property not found")
            )
        
        db.delete(property_model)
        db.commit()
        
        return create_success_response({"message": "Property deleted successfully"})
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=create_error_response(500, "Failed to delete property", {"exception": str(e)})
        )

@router.get("/stats/summary", response_model=PropertyStatsResponse)
async def get_property_stats(db: Session = Depends(get_db)):
    """Get property statistics summary"""
    
    try:
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
        
        stats_data = {
            "total_properties": total_properties,
            "property_types": [{"type": stat[0], "count": stat[1]} for stat in property_type_stats],
            "average_price": avg_price,
            "price_range": {
                "min": min_price,
                "max": max_price
            }
        }
        
        return PropertyStatsResponse(
            status="success",
            data=stats_data,
            error=None
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=create_error_response(500, "Failed to get property statistics", {"exception": str(e)})
        )