# Anand Jewels - Gold Rate Management System

A comprehensive jewelry business management system built with FastAPI, SQLite3, SQLAlchemy ORM, and Jinja2 Templates.

## Features

### Admin Dashboard (HTML via Jinja2)
- **Authentication**: Session-based login system
- **Gold Rate Management**: Complete CRUD operations for daily rates
- **Store Management**: Manage multiple store locations
- **Contact Enquiry Management**: Handle customer enquiries
- **Guide Management**: Educational content with image uploads
- **Responsive Design**: Bootstrap 5 with mobile-friendly interface
- **Statistics Dashboard**: Real-time business metrics

### Public JSON API
- **Gold Rates**: Latest rates, historical data, purity-based filtering
- **Store Information**: Get all stores and specific store details
- **Contact Enquiries**: Create customer enquiries
- **Educational Guides**: Access all guides and specific guide content
- **RESTful Design**: Comprehensive API with auto-documentation

## Tech Stack
- **FastAPI** - Modern Python web framework
- **SQLite3** - Lightweight database
- **SQLAlchemy ORM** - Database toolkit
- **Bootstrap 5** - Frontend framework
- **bcrypt** - Password hashing
- **Session-based auth** - Cookie middleware

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

3. Access the application:
- **Admin Dashboard**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/docs
- **API Base URL**: http://localhost:8000/api

## Default Credentials
- **Username**: admin
- **Password**: admin123

## API Endpoints

### Gold Rates
```
GET /api/gold-rates/latest                    # Latest rates for all purities
GET /api/gold-rates/history/7d               # Last 7 days history
GET /api/gold-rates/history/30d              # Last 30 days history
GET /api/gold-rates/history/{purity}?days=7  # Filter by purity (24K, 22K, 18K)
GET /api/gold-rates/purities                 # Available purities
```

### Stores
```
GET /api/stores                              # All store locations
GET /api/stores/{store_id}                   # Specific store details
```

### Contact Enquiries
```
POST /api/contact-enquiries                  # Create new enquiry
GET /api/contact-enquiries                   # All enquiries (admin)
GET /api/contact-enquiries/{enquiry_id}      # Specific enquiry
```

### Educational Guides
```
GET /api/guides                              # All guides
GET /api/guides/{guide_id}                   # Specific guide content
```

### System
```
GET /api/health                              # API health check
```

## Database Schema

### AdminUser
- id (Primary Key)
- username (Unique)
- password_hash (bcrypt)
- created_at (Auto timestamp)

### GoldRate
- id (Primary Key)
- purity (24K, 22K, 18K)
- new_rate_per_gram (Float)
- old_rate_per_gram (Float)
- release_datetime (DateTime)
- created_at (Auto timestamp)
- Unique constraint on (purity, release_datetime)

### Store
- id (Primary Key)
- store_name (String)
- store_address (String)
- store_image (String, optional)
- timings (String)
- created_at (Auto timestamp)

### ContactEnquiry
- id (Primary Key)
- name (String)
- phone_number (String)
- email (String)
- preferred_store (String)
- preferred_date_time (String)
- created_at (Auto timestamp)

### Guide
- id (Primary Key)
- title (String)
- content (Text)
- image (String, optional)
- created_at (Auto timestamp)

## Security Features
- bcrypt password hashing
- Session-based authentication
- Input validation
- SQL injection protection via ORM
- XSS protection in templates

## Development

The application automatically creates the SQLite database and tables on first run. The default admin user is also created automatically.

For production deployment:
1. Change the SECRET_KEY in main.py
2. Use environment variables for sensitive configuration
3. Consider using PostgreSQL instead of SQLite
4. Set up proper logging and monitoring

## Project Structure
```
project/
├── main.py              # FastAPI entrypoint
├── models.py            # SQLAlchemy models (5 tables)
├── database.py          # DB connection & initialization
├── auth.py              # Authentication logic
├── requirements.txt     # Dependencies
├── .gitignore          # Git ignore rules
├── README.md           # Project documentation
├── routers/
│   ├── admin.py        # Admin dashboard routes
│   ├── api.py          # Public API routes
│   └── stores.py       # Store & guide management
├── templates/
│   ├── base.html       # Bootstrap layout
│   ├── login.html      # Login form
│   ├── dashboard.html  # Dashboard home
│   ├── gold_rates/     # Gold rate templates
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── stores/         # Store management templates
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── enquiries/      # Contact enquiry templates
│   │   └── list.html
│   └── guides/         # Guide management templates
│       ├── list.html
│       ├── add.html
│       └── edit.html
└── static/
    ├── style.css       # Custom styles
    ├── dashboard.js    # Dashboard interactions
    └── images/
        ├── guides/     # Uploaded guide images
        └── stores/     # Store images
```

## File Upload Features
- **Image Upload**: Guides support image uploads with preview
- **File Validation**: Size (5MB) and format checking
- **Unique Naming**: UUID-based filenames prevent conflicts
- **Directory Structure**: Organized upload directories
- **Web Serving**: Static file serving for uploaded images