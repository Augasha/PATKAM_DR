#!/usr/bin/env python3
"""
Transport Database System Initialization Script
Creates and initializes the SQLite database with sample data
"""

import sqlite3
import os
from datetime import datetime, date, timedelta

def create_database():
    """Create the database and initialize with schema"""
    db_path = 'transport_system.db'
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read and execute schema
    with open('database_schema.sql', 'r') as f:
        schema = f.read()
    
    cursor.executescript(schema)
    print("Database schema created successfully")
    
    return conn, cursor

def insert_sample_data(cursor, conn):
    """Insert sample data for testing"""
    
    # Sample drivers
    drivers = [
        ('John', 'Smith', 'DL001', '555-0101', 'john.smith@email.com', '123 Main St', '1985-03-15', '2020-01-15', '2025-03-15', 'active'),
        ('Sarah', 'Johnson', 'DL002', '555-0102', 'sarah.j@email.com', '456 Oak Ave', '1990-07-22', '2019-06-01', '2024-07-22', 'active'),
        ('Mike', 'Wilson', 'DL003', '555-0103', 'mike.w@email.com', '789 Pine Rd', '1988-11-30', '2021-03-10', '2026-11-30', 'active'),
        ('Emily', 'Brown', 'DL004', '555-0104', 'emily.b@email.com', '321 Elm St', '1992-05-18', '2022-01-05', '2027-05-18', 'inactive')
    ]
    
    cursor.executemany('''
        INSERT INTO drivers (first_name, last_name, license_number, phone, email, address, 
                           date_of_birth, hire_date, license_expiry, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', drivers)
    
    # Sample vehicles
    vehicles = [
        ('Ford', 'Transit', 2020, 'ABC123', '1FTBW2CM5LKB12345', 'van', 2000, 'diesel', '2020-01-01', 35000.00, 45000, 'INS001', '2024-12-31', 'active'),
        ('Toyota', 'Camry', 2019, 'DEF456', '4T1B11HK8LU123456', 'car', 5, 'gasoline', '2019-06-01', 25000.00, 32000, 'INS002', '2024-06-30', 'active'),
        ('Freightliner', 'Cascadia', 2018, 'GHI789', '1FUJGBDV5JLP123456', 'truck', 40000, 'diesel', '2018-03-15', 120000.00, 150000, 'INS003', '2024-09-30', 'maintenance'),
        ('Honda', 'CR-V', 2021, 'JKL012', '2HKRW2H59MH123456', 'car', 5, 'gasoline', '2021-01-01', 28000.00, 18000, 'INS004', '2025-01-31', 'active')
    ]
    
    cursor.executemany('''
        INSERT INTO vehicles (make, model, year, license_plate, vin, vehicle_type, capacity, 
                             fuel_type, purchase_date, purchase_price, current_mileage, 
                             insurance_number, insurance_expiry, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', vehicles)
    
    # Sample routes
    routes = [
        ('Downtown to Airport', 'Downtown Station', 'International Airport', 25.5, 45, 'Main city route to airport', 1),
        ('Warehouse Route A', 'Central Warehouse', 'Distribution Center North', 15.2, 30, 'Daily warehouse supply route', 1),
        ('City Tour', 'Tourist Center', 'Historic District', 12.8, 25, 'Tourist circuit route', 1),
        ('Interstate Delivery', 'City Hub', 'Regional Distribution', 85.0, 90, 'Long-distance delivery route', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO routes (route_name, origin, destination, distance_km, estimated_duration_minutes, 
                           route_description, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', routes)
    
    # Sample trips
    trips = [
        (1, 1, 1, '2024-01-15', '08:00', '09:00', 45000, 45030, 25.5, 8.5, 'Passenger transport', 12, 0, 'completed', 'Regular morning run'),
        (2, 2, 2, '2024-01-15', '09:30', '10:15', 32000, 32020, 15.2, 4.2, 'Goods delivery', 0, 500, 'completed', 'Daily warehouse supply'),
        (1, 1, 3, '2024-01-15', '11:00', '11:40', 45030, 45050, 12.8, 4.1, 'Tour service', 8, 0, 'completed', 'City tour group'),
        (3, 3, 4, '2024-01-16', '06:00', '08:00', 150000, 150100, 85.0, 28.5, 'Freight delivery', 0, 15000, 'completed', 'Interstate freight')
    ]
    
    cursor.executemany('''
        INSERT INTO trips (driver_id, vehicle_id, route_id, trip_date, start_time, end_time, 
                          start_mileage, end_mileage, distance_covered, fuel_consumed, purpose, 
                          passenger_count, cargo_weight, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', trips)
    
    # Sample maintenance records
    maintenance = [
        (1, 'oil_change', 'Regular oil change service', 85.00, 45000, '2024-01-10', '2024-04-10', 50000, 'Quick Lube Service', '5W-30 Synthetic Oil', '6 months warranty'),
        (2, 'tire_rotation', 'Rotate all four tires', 45.00, 32000, '2024-01-08', '2024-07-08', 38000, 'Tire Plus', 'No new parts', '90 days'),
        (3, 'brake_service', 'Replace front brake pads', 320.00, 150000, '2024-01-12', '2024-07-12', 180000, 'Brake Masters', 'Front brake pads kit', '12 months'),
        (1, 'general_repair', 'Fix air conditioning system', 450.00, 45050, '2024-01-18', '2024-01-18', 45050, 'Auto AC Repair', 'AC compressor, refrigerant', '90 days')
    ]
    
    cursor.executemany('''
        INSERT INTO maintenance_records (vehicle_id, maintenance_type, description, cost, 
                                        mileage_at_service, service_date, next_service_date, 
                                        next_service_mileage, performed_by, parts_used, warranty_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', maintenance)
    
    # Sample fuel records
    fuel_records = [
        (1, 1, '2024-01-15', 'diesel', 40.5, 1.25, 50.63, 45030, 'Shell Station', 'Credit Card'),
        (2, 2, '2024-01-15', 'gasoline', 25.2, 1.35, 34.02, 32020, 'BP Gas', 'Debit Card'),
        (3, 3, '2024-01-16', 'diesel', 85.0, 1.22, 103.70, 150100, 'Pilot Travel Center', 'Company Card'),
        (1, 1, '2024-01-18', 'diesel', 35.8, 1.28, 45.82, 45080, 'Chevron', 'Credit Card')
    ]
    
    cursor.executemany('''
        INSERT INTO fuel_records (vehicle_id, driver_id, fuel_date, fuel_type, quantity_liters, 
                                  price_per_liter, total_cost, mileage, fuel_station, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', fuel_records)
    
    # Sample expenses
    expenses = [
        (1, 1, 'insurance', 'Monthly vehicle insurance premium', 250.00, '2024-01-01', 'INS001', 'SafeAuto Insurance'),
        (2, 2, 'tolls', 'Highway tolls for delivery route', 15.50, '2024-01-15', 'TOLL001', 'State Toll Authority'),
        (3, 3, 'parking', 'Overnight parking at distribution center', 25.00, '2024-01-16', 'PARK001', 'Secure Parking Co'),
        (None, None, 'registration', 'Annual vehicle registration fees', 450.00, '2024-01-10', 'REG001', 'DMV')
    ]
    
    cursor.executemany('''
        INSERT INTO expenses (vehicle_id, driver_id, expense_type, description, amount, 
                             expense_date, receipt_number, vendor)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', expenses)
    
    conn.commit()
    print("Sample data inserted successfully")

def main():
    """Main function to initialize the database"""
    print("Initializing Transport Database System...")
    
    try:
        conn, cursor = create_database()
        insert_sample_data(cursor, conn)
        
        print("\nDatabase initialization completed successfully!")
        print(f"Database file: transport_system.db")
        print("\nSample data includes:")
        print("- 4 drivers")
        print("- 4 vehicles") 
        print("- 4 routes")
        print("- 4 trips")
        print("- 4 maintenance records")
        print("- 4 fuel records")
        print("- 4 expense records")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
