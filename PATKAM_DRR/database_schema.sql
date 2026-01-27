-- Transport Database System Schema
-- Comprehensive system for managing drivers, vehicles, trips/routes, and maintenance records

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Drivers table
CREATE TABLE drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    date_of_birth DATE,
    hire_date DATE,
    license_expiry DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vehicles table
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    vin VARCHAR(17) UNIQUE,
    vehicle_type VARCHAR(30) NOT NULL CHECK (vehicle_type IN ('truck', 'van', 'car', 'bus', 'motorcycle')),
    capacity INTEGER,
    fuel_type VARCHAR(20) DEFAULT 'diesel' CHECK (fuel_type IN ('diesel', 'gasoline', 'electric', 'hybrid')),
    purchase_date DATE,
    purchase_price DECIMAL(10,2),
    current_mileage INTEGER DEFAULT 0,
    insurance_number VARCHAR(50),
    insurance_expiry DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'maintenance', 'retired', 'accident')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Routes table
CREATE TABLE routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_name VARCHAR(100) NOT NULL,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    distance_km DECIMAL(8,2),
    estimated_duration_minutes INTEGER,
    route_description TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trips table
CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    route_id INTEGER,
    trip_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    start_mileage INTEGER,
    end_mileage INTEGER,
    distance_covered DECIMAL(8,2),
    fuel_consumed DECIMAL(8,2),
    purpose VARCHAR(100),
    passenger_count INTEGER DEFAULT 0,
    cargo_weight DECIMAL(8,2),
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'in_progress', 'completed', 'cancelled')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE RESTRICT,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE RESTRICT,
    FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE SET NULL
);

-- Maintenance records table
CREATE TABLE maintenance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    maintenance_type VARCHAR(50) NOT NULL CHECK (maintenance_type IN ('oil_change', 'tire_rotation', 'brake_service', 'engine_service', 'transmission_service', 'general_repair', 'inspection', 'other')),
    description TEXT,
    cost DECIMAL(10,2),
    mileage_at_service INTEGER,
    service_date DATE NOT NULL,
    next_service_date DATE,
    next_service_mileage INTEGER,
    performed_by VARCHAR(100),
    parts_used TEXT,
    warranty_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
);

-- Fuel records table
CREATE TABLE fuel_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    driver_id INTEGER,
    fuel_date DATE NOT NULL,
    fuel_type VARCHAR(20) NOT NULL,
    quantity_liters DECIMAL(8,2) NOT NULL,
    price_per_liter DECIMAL(8,2) NOT NULL,
    total_cost DECIMAL(10,2) NOT NULL,
    mileage INTEGER,
    fuel_station VARCHAR(100),
    payment_method VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE SET NULL
);

-- Expenses table
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    driver_id INTEGER,
    expense_type VARCHAR(50) NOT NULL CHECK (expense_type IN ('fuel', 'maintenance', 'insurance', 'registration', 'tolls', 'parking', 'fines', 'other')),
    description TEXT,
    amount DECIMAL(10,2) NOT NULL,
    expense_date DATE NOT NULL,
    receipt_number VARCHAR(50),
    vendor VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL,
    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE SET NULL
);

-- Create indexes for better performance
CREATE INDEX idx_drivers_license ON drivers(license_number);
CREATE INDEX idx_vehicles_license_plate ON vehicles(license_plate);
CREATE INDEX idx_vehicles_vin ON vehicles(vin);
CREATE INDEX idx_trips_driver_id ON trips(driver_id);
CREATE INDEX idx_trips_vehicle_id ON trips(vehicle_id);
CREATE INDEX idx_trips_date ON trips(trip_date);
CREATE INDEX idx_maintenance_vehicle_id ON maintenance_records(vehicle_id);
CREATE INDEX idx_maintenance_date ON maintenance_records(service_date);
CREATE INDEX idx_fuel_vehicle_id ON fuel_records(vehicle_id);
CREATE INDEX idx_fuel_date ON fuel_records(fuel_date);
CREATE INDEX idx_expenses_vehicle_id ON expenses(vehicle_id);
CREATE INDEX idx_expenses_date ON expenses(expense_date);

-- Create triggers for automatic timestamp updates
CREATE TRIGGER update_drivers_timestamp 
    AFTER UPDATE ON drivers
    FOR EACH ROW
    BEGIN
        UPDATE drivers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER update_vehicles_timestamp 
    AFTER UPDATE ON vehicles
    FOR EACH ROW
    BEGIN
        UPDATE vehicles SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER update_routes_timestamp 
    AFTER UPDATE ON routes
    FOR EACH ROW
    BEGIN
        UPDATE routes SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER update_trips_timestamp 
    AFTER UPDATE ON trips
    FOR EACH ROW
    BEGIN
        UPDATE trips SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER update_maintenance_timestamp 
    AFTER UPDATE ON maintenance_records
    FOR EACH ROW
    BEGIN
        UPDATE maintenance_records SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
