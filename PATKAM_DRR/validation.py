"""
Data validation utilities for the Transport Database System
"""

import re
from datetime import datetime, date
from typing import Dict, Any, List, Optional

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class TransportValidator:
    """Validator for transport system data"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email:
            return True  # Email is optional
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        if not phone:
            return True  # Phone is optional
        # Remove common formatting characters
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        # Check if it's all digits and reasonable length
        return cleaned.isdigit() and len(cleaned) >= 10
    
    @staticmethod
    def validate_license_number(license_number: str) -> bool:
        """Validate driver license number format"""
        if not license_number:
            return False
        # Basic validation: alphanumeric, reasonable length
        return len(license_number.strip()) >= 3 and len(license_number.strip()) <= 50
    
    @staticmethod
    def validate_license_plate(license_plate: str) -> bool:
        """Validate vehicle license plate format"""
        if not license_plate:
            return False
        # Basic validation: alphanumeric, reasonable length
        return len(license_plate.strip()) >= 2 and len(license_plate.strip()) <= 20
    
    @staticmethod
    def validate_vin(vin: str) -> bool:
        """Validate VIN format"""
        if not vin:
            return True  # VIN is optional
        # VIN should be 17 characters (standard)
        cleaned = vin.replace('-', '').replace(' ', '').upper()
        return len(cleaned) == 17 and cleaned.isalnum()
    
    @staticmethod
    def validate_date(date_string: str) -> bool:
        """Validate date format and value"""
        if not date_string:
            return True  # Date is optional
        try:
            parsed_date = datetime.strptime(date_string, '%Y-%m-%d').date()
            # Check if date is reasonable (not too far in past or future)
            today = date.today()
            return date(1900, 1, 1) <= parsed_date <= date(today.year + 10, 12, 31)
        except ValueError:
            return False
    
    @staticmethod
    def validate_future_date(date_string: str) -> bool:
        """Validate that date is in the future"""
        if not date_string:
            return True  # Date is optional
        try:
            parsed_date = datetime.strptime(date_string, '%Y-%m-%d').date()
            return parsed_date >= date.today()
        except ValueError:
            return False
    
    @staticmethod
    def validate_year(year: int) -> bool:
        """Validate vehicle year"""
        current_year = date.today().year
        return 1900 <= year <= current_year + 1
    
    @staticmethod
    def validate_mileage(mileage: int) -> bool:
        """Validate mileage value"""
        return mileage >= 0 and mileage <= 10000000  # Reasonable upper limit
    
    @staticmethod
    def validate_cost(cost: float) -> bool:
        """Validate cost value"""
        return cost >= 0 and cost <= 1000000  # Reasonable upper limit
    
    @staticmethod
    def validate_fuel_quantity(quantity: float) -> bool:
        """Validate fuel quantity"""
        return quantity > 0 and quantity <= 10000  # Reasonable upper limit in liters
    
    @staticmethod
    def validate_distance(distance: float) -> bool:
        """Validate distance"""
        return distance >= 0 and distance <= 10000  # Reasonable upper limit in km
    
    @staticmethod
    def validate_passenger_count(count: int) -> bool:
        """Validate passenger count"""
        return count >= 0 and count <= 100  # Reasonable upper limit
    
    @staticmethod
    def validate_cargo_weight(weight: float) -> bool:
        """Validate cargo weight in kg"""
        return weight >= 0 and weight <= 100000  # Reasonable upper limit in kg

def validate_driver_data(data: Dict[str, Any]) -> List[str]:
    """Validate driver data and return list of errors"""
    errors = []
    
    # Required fields
    if not data.get('first_name') or len(data['first_name'].strip()) < 2:
        errors.append("First name is required and must be at least 2 characters")
    
    if not data.get('last_name') or len(data['last_name'].strip()) < 2:
        errors.append("Last name is required and must be at least 2 characters")
    
    if not TransportValidator.validate_license_number(data.get('license_number', '')):
        errors.append("Valid license number is required")
    
    # Optional fields validation
    if data.get('email') and not TransportValidator.validate_email(data['email']):
        errors.append("Invalid email format")
    
    if data.get('phone') and not TransportValidator.validate_phone(data['phone']):
        errors.append("Invalid phone number format")
    
    if data.get('date_of_birth') and not TransportValidator.validate_date(data['date_of_birth']):
        errors.append("Invalid date of birth format")
    
    if data.get('hire_date') and not TransportValidator.validate_date(data['hire_date']):
        errors.append("Invalid hire date format")
    
    if data.get('license_expiry') and not TransportValidator.validate_future_date(data['license_expiry']):
        errors.append("License expiry date must be in the future")
    
    # Status validation
    valid_statuses = ['active', 'inactive', 'suspended']
    if data.get('status') and data['status'] not in valid_statuses:
        errors.append("Invalid status value")
    
    return errors

def validate_vehicle_data(data: Dict[str, Any]) -> List[str]:
    """Validate vehicle data and return list of errors"""
    errors = []
    
    # Required fields
    if not data.get('make') or len(data['make'].strip()) < 2:
        errors.append("Vehicle make is required and must be at least 2 characters")
    
    if not data.get('model') or len(data['model'].strip()) < 2:
        errors.append("Vehicle model is required and must be at least 2 characters")
    
    if not data.get('year') or not TransportValidator.validate_year(data['year']):
        errors.append("Valid vehicle year is required")
    
    if not TransportValidator.validate_license_plate(data.get('license_plate', '')):
        errors.append("Valid license plate is required")
    
    if not data.get('vehicle_type'):
        errors.append("Vehicle type is required")
    
    # Optional fields validation
    if data.get('vin') and not TransportValidator.validate_vin(data['vin']):
        errors.append("Invalid VIN format (must be 17 alphanumeric characters)")
    
    if data.get('current_mileage') and not TransportValidator.validate_mileage(data['current_mileage']):
        errors.append("Invalid mileage value")
    
    if data.get('purchase_price') and not TransportValidator.validate_cost(data['purchase_price']):
        errors.append("Invalid purchase price")
    
    if data.get('purchase_date') and not TransportValidator.validate_date(data['purchase_date']):
        errors.append("Invalid purchase date format")
    
    if data.get('insurance_expiry') and not TransportValidator.validate_future_date(data['insurance_expiry']):
        errors.append("Insurance expiry date must be in the future")
    
    # Type validation
    valid_types = ['truck', 'van', 'car', 'bus', 'motorcycle']
    if data.get('vehicle_type') and data['vehicle_type'] not in valid_types:
        errors.append("Invalid vehicle type")
    
    valid_fuel_types = ['diesel', 'gasoline', 'electric', 'hybrid']
    if data.get('fuel_type') and data['fuel_type'] not in valid_fuel_types:
        errors.append("Invalid fuel type")
    
    valid_statuses = ['active', 'maintenance', 'retired', 'accident']
    if data.get('status') and data['status'] not in valid_statuses:
        errors.append("Invalid status value")
    
    return errors

def validate_trip_data(data: Dict[str, Any]) -> List[str]:
    """Validate trip data and return list of errors"""
    errors = []
    
    # Required fields
    if not data.get('driver_id'):
        errors.append("Driver is required")
    
    if not data.get('vehicle_id'):
        errors.append("Vehicle is required")
    
    if not data.get('trip_date'):
        errors.append("Trip date is required")
    elif not TransportValidator.validate_date(data['trip_date']):
        errors.append("Invalid trip date format")
    
    # Optional fields validation
    if data.get('start_mileage') and not TransportValidator.validate_mileage(data['start_mileage']):
        errors.append("Invalid start mileage value")
    
    if data.get('end_mileage') and not TransportValidator.validate_mileage(data['end_mileage']):
        errors.append("Invalid end mileage value")
    
    if data.get('distance_covered') and not TransportValidator.validate_distance(data['distance_covered']):
        errors.append("Invalid distance value")
    
    if data.get('fuel_consumed') and not TransportValidator.validate_fuel_quantity(data['fuel_consumed']):
        errors.append("Invalid fuel consumption value")
    
    if data.get('passenger_count') and not TransportValidator.validate_passenger_count(data['passenger_count']):
        errors.append("Invalid passenger count")
    
    if data.get('cargo_weight') and not TransportValidator.validate_cargo_weight(data['cargo_weight']):
        errors.append("Invalid cargo weight")
    
    # Logical validation
    if data.get('start_mileage') and data.get('end_mileage'):
        if data['end_mileage'] < data['start_mileage']:
            errors.append("End mileage cannot be less than start mileage")
    
    # Status validation
    valid_statuses = ['scheduled', 'in_progress', 'completed', 'cancelled']
    if data.get('status') and data['status'] not in valid_statuses:
        errors.append("Invalid status value")
    
    return errors

def validate_maintenance_data(data: Dict[str, Any]) -> List[str]:
    """Validate maintenance data and return list of errors"""
    errors = []
    
    # Required fields
    if not data.get('vehicle_id'):
        errors.append("Vehicle is required")
    
    if not data.get('maintenance_type'):
        errors.append("Maintenance type is required")
    
    if not data.get('service_date'):
        errors.append("Service date is required")
    elif not TransportValidator.validate_date(data['service_date']):
        errors.append("Invalid service date format")
    
    # Optional fields validation
    if data.get('mileage_at_service') and not TransportValidator.validate_mileage(data['mileage_at_service']):
        errors.append("Invalid mileage at service value")
    
    if data.get('cost') and not TransportValidator.validate_cost(data['cost']):
        errors.append("Invalid cost value")
    
    if data.get('next_service_date') and not TransportValidator.validate_date(data['next_service_date']):
        errors.append("Invalid next service date format")
    
    if data.get('next_service_mileage') and not TransportValidator.validate_mileage(data['next_service_mileage']):
        errors.append("Invalid next service mileage value")
    
    # Type validation
    valid_types = ['oil_change', 'tire_rotation', 'brake_service', 'engine_service', 
                   'transmission_service', 'general_repair', 'inspection', 'other']
    if data.get('maintenance_type') and data['maintenance_type'] not in valid_types:
        errors.append("Invalid maintenance type")
    
    return errors

def validate_route_data(data: Dict[str, Any]) -> List[str]:
    """Validate route data and return list of errors"""
    errors = []
    
    # Required fields
    if not data.get('route_name') or len(data['route_name'].strip()) < 3:
        errors.append("Route name is required and must be at least 3 characters")
    
    if not data.get('origin') or len(data['origin'].strip()) < 2:
        errors.append("Origin is required and must be at least 2 characters")
    
    if not data.get('destination') or len(data['destination'].strip()) < 2:
        errors.append("Destination is required and must be at least 2 characters")
    
    # Optional fields validation
    if data.get('distance_km') and not TransportValidator.validate_distance(data['distance_km']):
        errors.append("Invalid distance value")
    
    if data.get('estimated_duration_minutes'):
        try:
            duration = int(data['estimated_duration_minutes'])
            if duration <= 0 or duration > 1440:  # Max 24 hours
                errors.append("Estimated duration must be between 1 and 1440 minutes")
        except ValueError:
            errors.append("Invalid estimated duration format")
    
    return errors
