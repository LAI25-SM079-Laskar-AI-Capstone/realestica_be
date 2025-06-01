# ================================
# app/utils/responses.py
# ================================
from typing import Optional, Any

def create_error_response(code: int, message: str, details: Optional[dict] = None):
    error_data = {"code": code, "message": message}
    if details:
        error_data["details"] = details
    return {"status": "error", "data": None, "error": error_data}

def create_success_response(data: Any):
    return {"status": "success", "data": data, "error": None}

def parse_nearby_points_of_interest(poi_text: str) -> dict:
    """Parse nearby points of interest text into structured format"""
    if not poi_text:
        return {}
    
    result = {}
    
    # Split by semicolon to get different categories
    categories = [cat.strip() for cat in poi_text.split(';') if cat.strip()]
    
    for category in categories:
        if ':' in category:
            # Split category name and items
            category_name, items_str = category.split(':', 1)
            category_name = category_name.strip().lower()
            
            # Split items by comma and clean them
            items = [item.strip() for item in items_str.split(',') if item.strip()]
            
            if items:
                result[category_name] = items
    
    return result

def property_to_response(property_model) -> dict:
    from app.schemas.property import PropertyResponse, PropertySpecifications
    
    # Handle facilities field - convert string to list if needed
    facilities = []
    if property_model.facilities:
        if isinstance(property_model.facilities, list):
            # If it's already a list, flatten and clean each item
            for item in property_model.facilities:
                if isinstance(item, str):
                    # Split by semicolon and clean each facility
                    split_facilities = [facility.strip() for facility in item.split(';') if facility.strip()]
                    facilities.extend(split_facilities)
                else:
                    facilities.append(str(item))
        elif isinstance(property_model.facilities, str):
            # If it's a string, split by semicolon first, then by comma as fallback
            if ';' in property_model.facilities:
                facilities = [facility.strip() for facility in property_model.facilities.split(';') if facility.strip()]
            else:
                facilities = [facility.strip() for facility in property_model.facilities.split(',') if facility.strip()]
            
            # If no splitting worked, treat as single item
            if not facilities:
                facilities = [property_model.facilities.strip()]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_facilities = []
    for facility in facilities:
        if facility not in seen:
            seen.add(facility)
            unique_facilities.append(facility)
    
    # Parse nearby points of interest
    nearby_points_of_interest = parse_nearby_points_of_interest(
        property_model.nearby_points_of_interest_text or ""
    )
    
    specifications = PropertySpecifications(
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
        property_condition=property_model.property_condition
    )
    
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
        facilities=unique_facilities,
        specifications=specifications,
        nearby_points_of_interest=nearby_points_of_interest,
        createdAt=property_model.createdAt,
        updatedAt=property_model.updatedAt
    )