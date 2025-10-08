# Anand Jewels - Contact Enquiry Public API Documentation

## Base URL
```
http://your-domain.com/api
```

## Authentication
No authentication required for public API endpoints.

## Endpoints

### 1. Create Contact Enquiry
Create a new contact enquiry for jewelry consultation or appointment.

**Endpoint:** `POST /api/contact-enquiries`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John Doe",
  "phone_number": "9876543210",
  "email": "john.doe@example.com",
  "subject": "Wedding Jewelry Consultation",
  "preferred_store": "Anand Jewels Main Branch",
  "preferred_date_time": "2025-10-15 10:00 AM",
  "no_of_people": 2,
  "message": "Looking for traditional gold jewelry set for wedding ceremony"
}
```

**Field Validations:**
- `name`: Required, 2-100 characters
- `phone_number`: Required, 10-15 characters
- `email`: Required, valid email format
- `subject`: Optional, max 200 characters (default: "Contact enquiry")
- `preferred_store`: Required, 5-200 characters, must exist in stores
- `preferred_date_time`: Required, 10-100 characters
- `no_of_people`: Optional, integer 1-50 (default: 1)
- `message`: Optional, max 1000 characters (default: "NaN")

**Success Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "phone_number": "9876543210",
  "email": "john.doe@example.com",
  "subject": "Wedding Jewelry Consultation",
  "preferred_store": "Anand Jewels Main Branch",
  "preferred_date_time": "2025-10-15 10:00 AM",
  "no_of_people": 2,
  "message": "Looking for traditional gold jewelry set for wedding ceremony",
  "created_at": "2025-10-08T16:45:00"
}
```

**Error Responses:**

*400 Bad Request - Invalid Store:*
```json
{
  "detail": "Invalid store name. Available stores: Main Branch, Mall Branch, City Center"
}
```

*422 Unprocessable Entity - Validation Error:*
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 2. Get All Contact Enquiries
Retrieve all contact enquiries with optional limit.

**Endpoint:** `GET /api/contact-enquiries`

**Query Parameters:**
- `limit` (optional): Maximum number of enquiries to return (default: 50)

**Example Request:**
```
GET /api/contact-enquiries?limit=10
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "phone_number": "9876543210",
    "email": "john.doe@example.com",
    "subject": "Wedding Jewelry Consultation",
    "preferred_store": "Anand Jewels Main Branch",
    "preferred_date_time": "2025-10-15 10:00 AM",
    "no_of_people": 2,
    "message": "Looking for traditional gold jewelry set for wedding ceremony",
    "created_at": "2025-10-08T16:45:00"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "phone_number": "9876543211",
    "email": "jane.smith@example.com",
    "subject": "Gold Investment Query",
    "preferred_store": "Mall Branch",
    "preferred_date_time": "2025-10-16 2:00 PM",
    "no_of_people": 1,
    "message": "Interested in gold coins for investment",
    "created_at": "2025-10-08T17:30:00"
  }
]
```

### 3. Get Contact Enquiry by ID
Retrieve a specific contact enquiry by its ID.

**Endpoint:** `GET /api/contact-enquiries/{enquiry_id}`

**Path Parameters:**
- `enquiry_id`: Integer ID of the contact enquiry

**Example Request:**
```
GET /api/contact-enquiries/1
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Doe",
  "phone_number": "9876543210",
  "email": "john.doe@example.com",
  "subject": "Wedding Jewelry Consultation",
  "preferred_store": "Anand Jewels Main Branch",
  "preferred_date_time": "2025-10-15 10:00 AM",
  "no_of_people": 2,
  "message": "Looking for traditional gold jewelry set for wedding ceremony",
  "created_at": "2025-10-08T16:45:00"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Contact enquiry not found"
}
```

## Code Examples

### JavaScript/Fetch API
```javascript
// Create a new contact enquiry
async function createContactEnquiry() {
  try {
    const response = await fetch('/api/contact-enquiries', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: "John Doe",
        phone_number: "9876543210",
        email: "john.doe@example.com",
        subject: "Wedding Jewelry Consultation",
        preferred_store: "Anand Jewels Main Branch",
        preferred_date_time: "2025-10-15 10:00 AM",
        no_of_people: 2,
        message: "Looking for traditional gold jewelry set"
      })
    });

    if (response.ok) {
      const enquiry = await response.json();
      console.log('Enquiry created:', enquiry);
      return enquiry;
    } else {
      const error = await response.json();
      console.error('Error:', error);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}

// Get all enquiries
async function getAllEnquiries() {
  try {
    const response = await fetch('/api/contact-enquiries?limit=20');
    const enquiries = await response.json();
    console.log('All enquiries:', enquiries);
    return enquiries;
  } catch (error) {
    console.error('Error fetching enquiries:', error);
  }
}

// Get enquiry by ID
async function getEnquiryById(id) {
  try {
    const response = await fetch(`/api/contact-enquiries/${id}`);
    if (response.ok) {
      const enquiry = await response.json();
      console.log('Enquiry:', enquiry);
      return enquiry;
    } else if (response.status === 404) {
      console.log('Enquiry not found');
    }
  } catch (error) {
    console.error('Error fetching enquiry:', error);
  }
}
```

### cURL Examples
```bash
# Create contact enquiry
curl -X POST "http://your-domain.com/api/contact-enquiries" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone_number": "9876543210",
    "email": "john.doe@example.com",
    "subject": "Wedding Jewelry Consultation",
    "preferred_store": "Anand Jewels Main Branch",
    "preferred_date_time": "2025-10-15 10:00 AM",
    "no_of_people": 2,
    "message": "Looking for traditional gold jewelry set"
  }'

# Get all enquiries
curl "http://your-domain.com/api/contact-enquiries?limit=10"

# Get enquiry by ID
curl "http://your-domain.com/api/contact-enquiries/1"
```

### Python/Requests
```python
import requests
import json

# Create contact enquiry
def create_contact_enquiry():
    url = "http://your-domain.com/api/contact-enquiries"
    data = {
        "name": "John Doe",
        "phone_number": "9876543210",
        "email": "john.doe@example.com",
        "subject": "Wedding Jewelry Consultation",
        "preferred_store": "Anand Jewels Main Branch", 
        "preferred_date_time": "2025-10-15 10:00 AM",
        "no_of_people": 2,
        "message": "Looking for traditional gold jewelry set"
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 201:
        print("Enquiry created:", response.json())
        return response.json()
    else:
        print("Error:", response.json())

# Get all enquiries
def get_all_enquiries():
    url = "http://your-domain.com/api/contact-enquiries"
    params = {"limit": 20}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        enquiries = response.json()
        print(f"Found {len(enquiries)} enquiries")
        return enquiries
    else:
        print("Error:", response.status_code)

# Get enquiry by ID
def get_enquiry_by_id(enquiry_id):
    url = f"http://your-domain.com/api/contact-enquiries/{enquiry_id}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        enquiry = response.json()
        print("Enquiry found:", enquiry)
        return enquiry
    elif response.status_code == 404:
        print("Enquiry not found")
    else:
        print("Error:", response.status_code)
```

## Error Handling

### HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data or store name
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### Common Error Scenarios

1. **Invalid Store Name**: When preferred_store doesn't exist in the stores database
2. **Missing Required Fields**: When required fields like name, email, phone_number are missing
3. **Invalid Email Format**: When email doesn't match valid email pattern
4. **Field Length Validation**: When fields exceed maximum allowed length
5. **Invalid Number of People**: When no_of_people is less than 1 or greater than 50

## Rate Limiting
Currently no rate limiting is implemented. Consider implementing rate limiting for production use.

## CORS
Make sure CORS is properly configured to allow requests from your frontend domain.

## Security Considerations
- Input validation is implemented for all fields
- SQL injection protection through SQLAlchemy ORM
- Email validation to prevent invalid email addresses
- Store validation to ensure data integrity