#!/usr/bin/env python3
"""
Transport Database System - Flask Web Application
Provides REST API and web interface for managing transport operations
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime, date
import os
from validation import (
    validate_driver_data, validate_vehicle_data, validate_trip_data,
    validate_maintenance_data, validate_route_data, ValidationError
)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app)

# Database configuration
DATABASE = 'transport_system.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database if it doesn't exist"""
    if not os.path.exists(DATABASE):
        import subprocess
        subprocess.run(['python', 'init_database.py'])

# ==================== DRIVERS ENDPOINTS ====================

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/drivers')
def drivers_page():
    """Drivers management page"""
    return render_template('drivers.html')

@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    """Get all drivers"""
    conn = get_db_connection()
    drivers = conn.execute('SELECT * FROM drivers ORDER BY last_name, first_name').fetchall()
    conn.close()
    return jsonify([dict(driver) for driver in drivers])

@app.route('/api/drivers', methods=['POST'])
def create_driver():
    """Create a new driver"""
    data = request.get_json()
    
    # Validate data
    errors = validate_driver_data(data)
    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO drivers (first_name, last_name, license_number, phone, email, 
                               address, date_of_birth, hire_date, license_expiry, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['first_name'], data['last_name'], data['license_number'],
            data.get('phone'), data.get('email'), data.get('address'),
            data.get('date_of_birth'), data.get('hire_date'), 
            data.get('license_expiry'), data.get('status', 'active')
        ))
        
        conn.commit()
        driver_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'id': driver_id, 'message': 'Driver created successfully'}), 201
        
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({'error': 'License number already exists'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/drivers/<int:driver_id>', methods=['GET'])
def get_driver(driver_id):
    """Get a specific driver"""
    conn = get_db_connection()
    driver = conn.execute('SELECT * FROM drivers WHERE id = ?', (driver_id,)).fetchone()
    conn.close()
    
    if driver is None:
        return jsonify({'error': 'Driver not found'}), 404
    
    return jsonify(dict(driver))

@app.route('/api/drivers/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    """Update a driver"""
    data = request.get_json()
    
    # Validate data
    errors = validate_driver_data(data)
    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE drivers SET first_name=?, last_name=?, license_number=?, phone=?, email=?,
                             address=?, date_of_birth=?, hire_date=?, license_expiry=?, status=?
            WHERE id=?
        ''', (
            data['first_name'], data['last_name'], data['license_number'],
            data.get('phone'), data.get('email'), data.get('address'),
            data.get('date_of_birth'), data.get('hire_date'), 
            data.get('license_expiry'), data.get('status'), driver_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Driver updated successfully'})
        
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({'error': 'License number already exists'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/drivers/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    """Delete a driver"""
    conn = get_db_connection()
    
    # Check if driver has associated trips
    trips = conn.execute('SELECT COUNT(*) as count FROM trips WHERE driver_id = ?', (driver_id,)).fetchone()
    
    if trips['count'] > 0:
        conn.close()
        return jsonify({'error': 'Cannot delete driver with associated trips'}), 400
    
    conn.execute('DELETE FROM drivers WHERE id = ?', (driver_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Driver deleted successfully'})

# ==================== VEHICLES ENDPOINTS ====================

@app.route('/vehicles')
def vehicles_page():
    """Vehicles management page"""
    return render_template('vehicles.html')

@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    """Get all vehicles"""
    conn = get_db_connection()
    vehicles = conn.execute('SELECT * FROM vehicles ORDER BY make, model').fetchall()
    conn.close()
    return jsonify([dict(vehicle) for vehicle in vehicles])

@app.route('/api/vehicles', methods=['POST'])
def create_vehicle():
    """Create a new vehicle"""
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO vehicles (make, model, year, license_plate, vin, vehicle_type, capacity,
                                 fuel_type, purchase_date, purchase_price, current_mileage,
                                 insurance_number, insurance_expiry, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['make'], data['model'], data['year'], data['license_plate'],
            data.get('vin'), data['vehicle_type'], data.get('capacity'),
            data.get('fuel_type', 'diesel'), data.get('purchase_date'),
            data.get('purchase_price'), data.get('current_mileage', 0),
            data.get('insurance_number'), data.get('insurance_expiry'),
            data.get('status', 'active')
        ))
        
        conn.commit()
        vehicle_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'id': vehicle_id, 'message': 'Vehicle created successfully'}), 201
        
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({'error': 'License plate or VIN already exists'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    """Get a specific vehicle"""
    conn = get_db_connection()
    vehicle = conn.execute('SELECT * FROM vehicles WHERE id = ?', (vehicle_id,)).fetchone()
    conn.close()
    
    if vehicle is None:
        return jsonify({'error': 'Vehicle not found'}), 404
    
    return jsonify(dict(vehicle))

@app.route('/api/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    """Update a vehicle"""
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE vehicles SET make=?, model=?, year=?, license_plate=?, vin=?, vehicle_type=?,
                               capacity=?, fuel_type=?, purchase_date=?, purchase_price=?,
                               current_mileage=?, insurance_number=?, insurance_expiry=?, status=?
            WHERE id=?
        ''', (
            data['make'], data['model'], data['year'], data['license_plate'],
            data.get('vin'), data['vehicle_type'], data.get('capacity'),
            data.get('fuel_type'), data.get('purchase_date'), data.get('purchase_price'),
            data.get('current_mileage'), data.get('insurance_number'),
            data.get('insurance_expiry'), data.get('status'), vehicle_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Vehicle updated successfully'})
        
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({'error': 'License plate or VIN already exists'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    """Delete a vehicle"""
    conn = get_db_connection()
    
    # Check if vehicle has associated records
    trips = conn.execute('SELECT COUNT(*) as count FROM trips WHERE vehicle_id = ?', (vehicle_id,)).fetchone()
    maintenance = conn.execute('SELECT COUNT(*) as count FROM maintenance_records WHERE vehicle_id = ?', (vehicle_id,)).fetchone()
    
    if trips['count'] > 0 or maintenance['count'] > 0:
        conn.close()
        return jsonify({'error': 'Cannot delete vehicle with associated records'}), 400
    
    conn.execute('DELETE FROM vehicles WHERE id = ?', (vehicle_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Vehicle deleted successfully'})

# ==================== TRIPS ENDPOINTS ====================

@app.route('/trips')
def trips_page():
    """Trips management page"""
    return render_template('trips.html')

@app.route('/api/trips', methods=['GET'])
def get_trips():
    """Get all trips with driver and vehicle info"""
    conn = get_db_connection()
    trips = conn.execute('''
        SELECT t.*, d.first_name || ' ' || d.last_name as driver_name,
               v.make || ' ' || v.model as vehicle_name, v.license_plate,
               r.route_name
        FROM trips t
        LEFT JOIN drivers d ON t.driver_id = d.id
        LEFT JOIN vehicles v ON t.vehicle_id = v.id
        LEFT JOIN routes r ON t.route_id = r.id
        ORDER BY t.trip_date DESC, t.start_time DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(trip) for trip in trips])

@app.route('/api/trips', methods=['POST'])
def create_trip():
    """Create a new trip"""
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO trips (driver_id, vehicle_id, route_id, trip_date, start_time, end_time,
                              start_mileage, end_mileage, distance_covered, fuel_consumed,
                              purpose, passenger_count, cargo_weight, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['driver_id'], data['vehicle_id'], data.get('route_id'),
            data['trip_date'], data.get('start_time'), data.get('end_time'),
            data.get('start_mileage'), data.get('end_mileage'),
            data.get('distance_covered'), data.get('fuel_consumed'),
            data.get('purpose'), data.get('passenger_count', 0),
            data.get('cargo_weight'), data.get('status', 'scheduled'),
            data.get('notes')
        ))
        
        conn.commit()
        trip_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'id': trip_id, 'message': 'Trip created successfully'}), 201
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/trips/<int:trip_id>', methods=['PUT'])
def update_trip(trip_id):
    """Update a trip"""
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE trips SET driver_id=?, vehicle_id=?, route_id=?, trip_date=?, start_time=?,
                              end_time=?, start_mileage=?, end_mileage=?, distance_covered=?,
                              fuel_consumed=?, purpose=?, passenger_count=?, cargo_weight=?,
                              status=?, notes=?
            WHERE id=?
        ''', (
            data['driver_id'], data['vehicle_id'], data.get('route_id'),
            data['trip_date'], data.get('start_time'), data.get('end_time'),
            data.get('start_mileage'), data.get('end_mileage'),
            data.get('distance_covered'), data.get('fuel_consumed'),
            data.get('purpose'), data.get('passenger_count'),
            data.get('cargo_weight'), data.get('status'), data.get('notes'), trip_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Trip updated successfully'})
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/trips/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    """Delete a trip"""
    conn = get_db_connection()
    conn.execute('DELETE FROM trips WHERE id = ?', (trip_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Trip deleted successfully'})

# ==================== MAINTENANCE ENDPOINTS ====================

@app.route('/maintenance')
def maintenance_page():
    """Maintenance management page"""
    return render_template('maintenance.html')

@app.route('/api/maintenance', methods=['GET'])
def get_maintenance():
    """Get all maintenance records with vehicle info"""
    conn = get_db_connection()
    maintenance = conn.execute('''
        SELECT m.*, v.make || ' ' || v.model as vehicle_name, v.license_plate
        FROM maintenance_records m
        LEFT JOIN vehicles v ON m.vehicle_id = v.id
        ORDER BY m.service_date DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(record) for record in maintenance])

@app.route('/api/maintenance', methods=['POST'])
def create_maintenance():
    """Create a new maintenance record"""
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO maintenance_records (vehicle_id, maintenance_type, description, cost,
                                           mileage_at_service, service_date, next_service_date,
                                           next_service_mileage, performed_by, parts_used, warranty_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['vehicle_id'], data['maintenance_type'], data.get('description'),
            data.get('cost'), data.get('mileage_at_service'), data['service_date'],
            data.get('next_service_date'), data.get('next_service_mileage'),
            data.get('performed_by'), data.get('parts_used'), data.get('warranty_info')
        ))
        
        conn.commit()
        maintenance_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'id': maintenance_id, 'message': 'Maintenance record created successfully'}), 201
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/maintenance/<int:maintenance_id>', methods=['PUT'])
def update_maintenance(maintenance_id):
    """Update a maintenance record"""
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE maintenance_records SET vehicle_id=?, maintenance_type=?, description=?,
                                             cost=?, mileage_at_service=?, service_date=?,
                                             next_service_date=?, next_service_mileage=?,
                                             performed_by=?, parts_used=?, warranty_info=?
            WHERE id=?
        ''', (
            data['vehicle_id'], data['maintenance_type'], data.get('description'),
            data.get('cost'), data.get('mileage_at_service'), data['service_date'],
            data.get('next_service_date'), data.get('next_service_mileage'),
            data.get('performed_by'), data.get('parts_used'), data.get('warranty_info'),
            maintenance_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Maintenance record updated successfully'})
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/maintenance/<int:maintenance_id>', methods=['DELETE'])
def delete_maintenance(maintenance_id):
    """Delete a maintenance record"""
    conn = get_db_connection()
    conn.execute('DELETE FROM maintenance_records WHERE id = ?', (maintenance_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Maintenance record deleted successfully'})

# ==================== DASHBOARD ENDPOINTS ====================

@app.route('/api/dashboard/stats')
def get_dashboard_stats():
    """Get dashboard statistics"""
    conn = get_db_connection()
    
    # Get counts
    drivers_count = conn.execute('SELECT COUNT(*) as count FROM drivers WHERE status = "active"').fetchone()
    vehicles_count = conn.execute('SELECT COUNT(*) as count FROM vehicles WHERE status = "active"').fetchone()
    trips_today = conn.execute('SELECT COUNT(*) as count FROM trips WHERE trip_date = ?', (date.today(),)).fetchone()
    maintenance_due = conn.execute('''
        SELECT COUNT(*) as count FROM maintenance_records 
        WHERE next_service_date <= date('now', '+7 days')
    ''').fetchone()
    
    # Get recent trips
    recent_trips = conn.execute('''
        SELECT t.*, d.first_name || ' ' || d.last_name as driver_name,
               v.make || ' ' || v.model as vehicle_name
        FROM trips t
        LEFT JOIN drivers d ON t.driver_id = d.id
        LEFT JOIN vehicles v ON t.vehicle_id = v.id
        ORDER BY t.trip_date DESC, t.start_time DESC
        LIMIT 5
    ''').fetchall()
    
    # Get upcoming maintenance
    upcoming_maintenance = conn.execute('''
        SELECT m.*, v.make || ' ' || v.model as vehicle_name, v.license_plate
        FROM maintenance_records m
        LEFT JOIN vehicles v ON m.vehicle_id = v.id
        WHERE m.next_service_date <= date('now', '+30 days')
        ORDER BY m.next_service_date ASC
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        'stats': {
            'active_drivers': drivers_count['count'],
            'active_vehicles': vehicles_count['count'],
            'trips_today': trips_today['count'],
            'maintenance_due': maintenance_due['count']
        },
        'recent_trips': [dict(trip) for trip in recent_trips],
        'upcoming_maintenance': [dict(record) for record in upcoming_maintenance]
    })

# ==================== ROUTES ENDPOINTS ====================

@app.route('/api/routes', methods=['GET'])
def get_routes():
    """Get all routes"""
    conn = get_db_connection()
    routes = conn.execute('SELECT * FROM routes WHERE is_active = 1 ORDER BY route_name').fetchall()
    conn.close()
    return jsonify([dict(route) for route in routes])

@app.route('/api/routes', methods=['POST'])
def create_route():
    """Create a new route"""
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO routes (route_name, origin, destination, distance_km, 
                               estimated_duration_minutes, route_description, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['route_name'], data['origin'], data['destination'],
            data.get('distance_km'), data.get('estimated_duration_minutes'),
            data.get('route_description'), data.get('is_active', 1)
        ))
        
        conn.commit()
        route_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'id': route_id, 'message': 'Route created successfully'}), 201
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
