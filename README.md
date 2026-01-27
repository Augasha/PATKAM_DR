# Transport Database System

A comprehensive transport management system for tracking drivers, vehicles, trips/routes, and maintenance records. Built with Flask, SQLite, and Bootstrap.

## Features

- **Driver Management**: Add, edit, and manage driver records with license tracking
- **Vehicle Management**: Track vehicle information, mileage, insurance, and status
- **Trip Management**: Log trips with drivers, vehicles, routes, and fuel consumption
- **Maintenance Records**: Track vehicle maintenance schedules and service history
- **Dashboard**: Overview with statistics and recent activity
- **Data Validation**: Comprehensive input validation and error handling
- **Responsive Design**: Mobile-friendly web interface

## System Requirements

- Python 3.7 or higher
- SQLite3 (included with Python)
- Modern web browser

## Installation

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd transport-database-system
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python init_database.py
   ```
   This will create the SQLite database with sample data.

## Running the Application

1. **Start the web server**
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

The application will be available at `http://localhost:5000` and will automatically create the database if it doesn't exist.

## Database Structure

The system uses SQLite with the following main tables:

### Drivers
- Personal information (name, contact details)
- License information and expiry dates
- Employment status and hire dates

### Vehicles
- Vehicle details (make, model, year, VIN)
- License plates and insurance information
- Current mileage and status tracking

### Trips
- Trip scheduling and execution tracking
- Driver and vehicle assignments
- Distance, fuel consumption, and cargo/passenger data
- Route information and trip status

### Maintenance Records
- Service history and scheduling
- Maintenance types and costs
- Parts used and warranty information
- Next service reminders

### Supporting Tables
- **Routes**: Predefined routes with distances and estimated times
- **Fuel Records**: Fuel purchases and consumption tracking
- **Expenses**: General expense tracking for vehicles and operations

## API Endpoints

The system provides RESTful API endpoints for all operations:

### Drivers
- `GET /api/drivers` - List all drivers
- `POST /api/drivers` - Create new driver
- `GET /api/drivers/<id>` - Get specific driver
- `PUT /api/drivers/<id>` - Update driver
- `DELETE /api/drivers/<id>` - Delete driver

### Vehicles
- `GET /api/vehicles` - List all vehicles
- `POST /api/vehicles` - Create new vehicle
- `GET /api/vehicles/<id>` - Get specific vehicle
- `PUT /api/vehicles/<id>` - Update vehicle
- `DELETE /api/vehicles/<id>` - Delete vehicle

### Trips
- `GET /api/trips` - List all trips with driver/vehicle details
- `POST /api/trips` - Create new trip
- `PUT /api/trips/<id>` - Update trip
- `DELETE /api/trips/<id>` - Delete trip

### Maintenance
- `GET /api/maintenance` - List all maintenance records
- `POST /api/maintenance` - Create maintenance record
- `PUT /api/maintenance/<id>` - Update maintenance record
- `DELETE /api/maintenance/<id>` - Delete maintenance record

### Routes
- `GET /api/routes` - List all active routes
- `POST /api/routes` - Create new route

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics and recent activity

## Web Interface

The web application provides an intuitive interface with the following pages:

### Dashboard (`/`)
- Overview statistics (active drivers, vehicles, today's trips, maintenance due)
- Recent trips table
- Upcoming maintenance reminders

### Drivers (`/drivers`)
- Complete driver management interface
- Add/edit/delete drivers
- License expiry tracking
- Status management

### Vehicles (`/vehicles`)
- Vehicle fleet management
- Insurance tracking
- Mileage monitoring
- Status updates

### Trips (`/trips`)
- Trip scheduling and logging
- Driver and vehicle assignment
- Route management
- Fuel and distance tracking

### Maintenance (`/maintenance`)
- Service record management
- Maintenance scheduling
- Cost tracking
- Parts and warranty information

## Data Validation

The system includes comprehensive validation:

### Driver Validation
- Name fields (2+ characters required)
- License number format and uniqueness
- Email format validation
- Phone number format
- Date validation and logical checks

### Vehicle Validation
- Make/model requirements
- Year range validation (1900-current year + 1)
- License plate format and uniqueness
- VIN format (17 characters)
- Mileage and cost limits

### Trip Validation
- Required driver and vehicle assignments
- Date and time validation
- Logical mileage checks (end ≥ start)
- Distance and fuel consumption limits

### Maintenance Validation
- Required vehicle and service type
- Date validation
- Cost and mileage limits
- Service type validation

## Sample Data

The initialization script creates sample data including:
- 4 drivers with various statuses
- 4 vehicles (truck, van, cars)
- 4 predefined routes
- Sample trips with fuel consumption data
- Maintenance records with different service types
- Fuel and expense records

## Security Considerations

- Input validation on all data entry points
- SQL injection prevention through parameterized queries
- Data integrity constraints in the database
- Status-based record deletion protection

## Backup and Recovery

### Database Backup
```bash
# Create backup
cp transport_system.db transport_system_backup_$(date +%Y%m%d).db

# Or using SQLite dump
sqlite3 transport_system.db .dump > backup_$(date +%Y%m%d).sql
```

### Database Recovery
```bash
# Restore from backup file
cp transport_system_backup_YYYYMMDD.db transport_system.db

# Or restore from SQL dump
sqlite3 transport_system.db < backup_YYYYMMDD.sql
```

## Troubleshooting

### Common Issues

1. **Database locked error**
   - Ensure only one instance of the application is running
   - Check for other processes accessing the database

2. **Port 5000 already in use**
   - Change the port in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

3. **Missing dependencies**
   - Install required packages: `pip install -r requirements.txt`

4. **Database not found**
   - Run the initialization script: `python init_database.py`

### Logs and Debugging

The Flask application runs in debug mode by default, providing:
- Detailed error messages
- Interactive debugger
- Auto-reload on code changes

For production deployment, disable debug mode:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Development

### Project Structure
```
transport-database-system/
├── app.py                 # Main Flask application
├── database_schema.sql    # Database schema definition
├── init_database.py      # Database initialization script
├── validation.py         # Data validation utilities
├── requirements.txt      # Python dependencies
├── transport_system.db   # SQLite database (created by init script)
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Dashboard page
│   ├── drivers.html     # Drivers management
│   ├── vehicles.html    # Vehicles management
│   ├── trips.html       # Trips management
│   └── maintenance.html # Maintenance records
└── README.md           # This file
```

### Adding New Features

1. **Database Changes**: Modify `database_schema.sql`
2. **API Endpoints**: Add routes in `app.py`
3. **Validation**: Add validation rules in `validation.py`
4. **Frontend**: Create/modify templates in `templates/`

## License

This project is provided as-is for educational and demonstration purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the error messages in the browser console
3. Verify database integrity and permissions
4. Ensure all dependencies are properly installed
