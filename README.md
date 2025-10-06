# Anand Jewels - Complete Jewelry Business Management System

A comprehensive jewelry business management system built with FastAPI, SQLite3, SQLAlchemy ORM, Alembic migrations, and Jinja2 Templates with Bootstrap 5 UI.

## Features

### Admin Dashboard (HTML via Jinja2)
- **Authentication**: JWT-based login system with session management
- **Gold Rate Management**: Complete CRUD operations for multi-purity rates (24K, 22K, 18K)
- **Store Management**: Manage multiple store locations with images and timings
- **Contact Enquiry Management**: Handle customer enquiries with subject categorization
- **Content Management**: About, Team, Mission, Terms & Conditions, Vision pages
- **Guide Management**: Educational content with image uploads
- **Award & Achievement Management**: Company recognition and milestone tracking
- **Notification System**: Announcement and update management
- **Responsive Design**: Bootstrap 5 with professional UI components
- **Statistics Dashboard**: Real-time business metrics and comprehensive analytics

### Public JSON API
- **Gold Rates**: Latest rates, historical data, purity-based filtering, pagination
- **Store Information**: Complete store directory with contact details and timings
- **Contact Enquiries**: Create customer enquiries with subject categorization
- **Content APIs**: About, Team, Mission, Terms, Vision, and Guide content
- **Awards & Achievements**: Public access to company recognition and milestones
- **Notifications**: Latest announcements and updates
- **RESTful Design**: Comprehensive API with auto-documentation and health checks

## Tech Stack
- **FastAPI** - Modern Python web framework with automatic API docs
- **SQLite3** - Lightweight database (production-ready with PostgreSQL support)
- **SQLAlchemy ORM** - Database toolkit with relationship management
- **Alembic** - Database migration tool for schema versioning
- **Bootstrap 5** - Modern responsive frontend framework
- **Jinja2** - Template engine for server-side rendering
- **JWT + Sessions** - Dual authentication system
- **bcrypt** - Secure password hashing
- **Pydantic** - Data validation and serialization

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd anand-jeweller-backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Initialize database:**
```bash
# Run initial migration to create tables
alembic upgrade head
```

5. **Start the application:**
```bash
python start_server.py
# or
python main.py
```

6. **Access the application:**
- **Admin Dashboard**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/docs
- **Public API**: http://localhost:8000/api


## API Endpoints

### Gold Rates
```
GET /api/gold-rates/latest                    # Latest rates for all purities
GET /api/gold-rates/current                  # Current rates (simplified format)
GET /api/gold-rates/history/7d               # Last 7 days history
GET /api/gold-rates/history/30d              # Last 30 days history
GET /api/gold-rates/history/{purity}?days=7  # Filter by purity (24K, 22K, 18K)
GET /api/gold-rates/all?page=1&limit=10      # All rates with pagination
GET /api/gold-rates/purities                 # Available purities
```

### Stores
```
GET /api/stores                              # All store locations
GET /api/stores/{store_id}                   # Specific store details
```

### Contact Enquiries
```
POST /api/contact-enquiries                  # Create new enquiry with subject
GET /api/contact-enquiries                   # All enquiries (limited for performance)
GET /api/contact-enquiries/{enquiry_id}      # Specific enquiry details
```

### Content Management
```
GET /api/about                               # All about us entries
GET /api/about/{about_id}                    # Specific about entry
GET /api/team                                # All team members
GET /api/team/{team_id}                      # Specific team member
GET /api/missions                            # All mission entries
GET /api/missions/{mission_id}               # Specific mission
GET /api/terms                               # All terms & conditions
GET /api/terms/{terms_id}                    # Specific terms entry
GET /api/visions                             # All vision entries
GET /api/visions/{vision_id}                 # Specific vision entry
GET /api/guides                              # All educational guides
GET /api/guides/{guide_id}                   # Specific guide content
```

### Awards & Achievements
```
GET /api/awards                              # All company awards
GET /api/awards/{award_id}                   # Specific award details
GET /api/achievements                        # All achievements with images
GET /api/achievements/{achievement_id}       # Specific achievement details
```

### Notifications
```
GET /api/notifications                       # All notifications (latest first)
GET /api/notifications/{notification_id}     # Specific notification
```

### System
```
GET /api                                     # Complete API documentation
GET /api/health                              # API health check
```

## Database Schema (14 Tables)

### Core System Tables

#### AdminUser
- id (Primary Key)
- username (Unique)
- password_hash (bcrypt)

#### GoldRate (Consolidated Multi-Purity)
- id (Primary Key)
- gold_24k_new_rate, gold_24k_exchange_rate, gold_24k_making_charges
- gold_22k_new_rate, gold_22k_exchange_rate, gold_22k_making_charges  
- gold_18k_new_rate, gold_18k_exchange_rate, gold_18k_making_charges
- release_datetime (DateTime, Unique)
- created_at (Auto timestamp)

### Business Management Tables

#### Store
- id (Primary Key)
- store_name, phone_number, store_address
- store_image, youtube_link, timings
- created_at (Auto timestamp)

#### ContactEnquiry
- id (Primary Key)
- name, phone_number, email
- **subject** (Optional, default: "Contact enquiry")
- preferred_store, preferred_date_time
- created_at (Auto timestamp)

### Content Management Tables

#### About
- id, title, content, image, created_at

#### Team  
- id, position, name, content, image, created_at

#### Mission
- id, title, content, image, created_at

#### Terms
- id, title, content, image, created_at

#### Vision
- id, title, content, image, created_at

#### Guide
- id, title, content, image, created_at

### Recognition & Communication Tables

#### Award
- id (Primary Key)
- title, content
- created_at (Auto timestamp)

#### Achievement
- id (Primary Key)
- title, date (Achievement date)
- content, image
- created_at (Auto timestamp)

#### Notification
- id (Primary Key)
- title, description
- datetime (Notification date/time)
- created_at (Auto timestamp)

## Database Migrations (Alembic)

This project uses Alembic for database schema versioning and migrations.

### Migration Commands

**Initialize Alembic (if not already done):**
```bash
alembic init alembic
```

**Create a new migration:**
```bash
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations:**
```bash
alembic upgrade head
```

**View migration history:**
```bash
alembic history
alembic current
```

**Rollback migrations:**
```bash
alembic downgrade -1      # Rollback one migration
alembic downgrade <revision_id>  # Rollback to specific revision
```

### Migration History
- Initial schema with core tables (AdminUser, GoldRate, Store, ContactEnquiry, Guide)
- Added content management tables (About, Team, Mission, Terms, Vision)
- Added Awards, Achievements, and Notifications tables
- Added subject field to ContactEnquiry table

### Database Configuration
- **Development**: SQLite3 (`gold_rates.db`)
- **Production**: Configurable for PostgreSQL/MySQL
- **Migrations**: Tracked in `alembic/versions/`
- **Auto-generation**: Schema changes detected automatically

## Security Features
- JWT token authentication with session fallback
- bcrypt password hashing (cost factor 12)
- Input validation with Pydantic models
- SQL injection protection via SQLAlchemy ORM
- XSS protection in Jinja2 templates
- File upload validation and security
- Admin route protection with dependency injection

## Development

### Database Setup
The application uses Alembic for database management:
1. Database schema is created via migrations
2. Default admin user is created automatically
3. All schema changes are tracked and versioned

### Development Workflow
```bash
# Make model changes in models.py
# Generate migration
alembic revision --autogenerate -m "Your change description"

# Review the generated migration file
# Apply the migration
alembic upgrade head

# Start development server
python start_server.py
```

### Production Deployment
1. **Environment Configuration:**
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export DATABASE_URL="postgresql://user:pass@host:port/dbname"
   ```

2. **Database Setup:**
   ```bash
   alembic upgrade head  # Apply all migrations
   ```

3. **Security Checklist:**
   - Change default admin credentials
   - Use environment variables for secrets
   - Enable HTTPS in production
   - Configure proper CORS settings
   - Set up database backups
   - Monitor application logs

4. **Scaling Considerations:**
   - Use PostgreSQL for production
   - Configure connection pooling
   - Set up reverse proxy (Nginx)
   - Enable static file serving
   - Configure file upload limits

## Project Structure
```
project/
├── main.py                 # FastAPI application entrypoint
├── start_server.py         # Server startup script
├── models.py               # SQLAlchemy models (14 tables)
├── database.py             # Database connection & initialization
├── auth.py                 # Session-based authentication
├── jwt_auth.py             # JWT token authentication
├── requirements.txt        # Python dependencies
├── alembic.ini            # Alembic configuration
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
├── gold_rates.db          # SQLite database file
├── alembic/               # Database migrations
│   ├── env.py             # Alembic environment
│   ├── script.py.mako     # Migration template
│   └── versions/          # Migration files
│       ├── initial_schema.py
│       ├── content_tables.py
│       ├── awards_achievements.py
│       └── contact_subject.py
├── routers/
│   ├── __init__.py
│   ├── admin.py           # Admin dashboard routes (CRUD for all modules)
│   ├── admin_api.py       # Admin API endpoints
│   ├── api.py             # Public JSON API
│   └── stores.py          # Store-specific routes
├── templates/
│   ├── base.html          # Bootstrap 5 responsive layout
│   ├── login.html         # Modern login interface
│   ├── dashboard.html     # Statistics dashboard
│   ├── gold_rates/        # Gold rate management
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── stores/            # Store management
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── contact_enquiries/ # Customer enquiry management
│   │   ├── list.html
│   │   └── view.html
│   ├── guides/            # Educational content
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── about/             # About us management
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── team/              # Team management
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── missions/          # Mission management
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── terms/             # Terms & conditions
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── visions/           # Vision management
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── awards/            # Awards management
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── achievements/      # Achievements with images
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   └── notifications/     # Notification system
│       ├── list.html
│       ├── add.html
│       └── edit.html
└── static/
    ├── style.css          # Custom Bootstrap styles
    ├── dashboard.js       # Interactive dashboard
    ├── css/               # Additional stylesheets
    ├── images/            # Static images
    │   ├── footer-logo.png
    │   ├── guides/        # Uploaded guide images
    │   └── stores/        # Store images
    └── uploads/           # User uploaded files
        ├── about/         # About us images
        ├── team/          # Team member photos
        ├── missions/      # Mission images
        ├── terms/         # Terms images
        ├── visions/       # Vision images
        ├── achievements/  # Achievement images
        ├── guides/        # Guide images
        └── stores/        # Store images
```

## File Upload Features
- **Multi-Module Support**: Image uploads for Guides, Stores, About, Team, Missions, Terms, Vision, and Achievements
- **File Validation**: Size limits (5MB default) and format checking (JPEG, PNG, GIF)
- **Secure Storage**: UUID-based filenames prevent conflicts and directory traversal
- **Organized Structure**: Module-specific upload directories (`static/uploads/{module}/`)
- **Web Serving**: Efficient static file serving for all uploaded images
- **Image Management**: Upload, replace, and delete functionality with admin interface

## Admin Dashboard Features
- **Modern UI**: Professional Bootstrap 5 interface with responsive design
- **Comprehensive CRUD**: Full Create, Read, Update, Delete operations for all modules
- **File Management**: Drag-and-drop file uploads with preview functionality
- **Data Validation**: Client-side and server-side validation for all forms
- **Search & Filter**: Advanced filtering and search capabilities
- **Export Options**: Data export functionality for reports
- **Real-time Stats**: Live dashboard with business metrics and analytics
- **User Management**: Secure admin authentication with session management

## API Features
- **RESTful Design**: Consistent REST API patterns across all endpoints
- **Auto Documentation**: Interactive API docs with Swagger UI at `/docs`
- **Data Validation**: Pydantic models for request/response validation
- **Error Handling**: Comprehensive error responses with proper HTTP status codes
- **Pagination**: Built-in pagination for large data sets
- **Filtering**: Advanced filtering options for data queries
- **Rate Limiting**: Configurable rate limiting for API protection
- **CORS Support**: Cross-origin resource sharing for web applications