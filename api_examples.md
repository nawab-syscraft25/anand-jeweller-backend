# Anand Jewels API Examples

## Store Management APIs

### Get All Stores
```bash
curl -X GET "http://localhost:8000/api/stores" \
  -H "accept: application/json"
```

**Response:**
```json
[
  {
    "id": 1,
    "store_name": "Anand Jewels - Main Branch",
    "store_address": "123 Gold Street, Jewelry District, Mumbai - 400001",
    "store_image": "/static/images/store1.jpg",
    "timings": "Mon-Sat: 10:00 AM - 8:00 PM, Sun: 11:00 AM - 6:00 PM",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

### Get Specific Store
```bash
curl -X GET "http://localhost:8000/api/stores/1" \
  -H "accept: application/json"
```

## Contact Enquiry APIs

### Create Contact Enquiry
```bash
curl -X POST "http://localhost:8000/api/contact-enquiries" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone_number": "+91 9876543210",
    "email": "john.doe@example.com",
    "preferred_store": "Anand Jewels - Main Branch",
    "preferred_date_time": "2024-01-20 at 3:00 PM"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "phone_number": "+91 9876543210",
  "email": "john.doe@example.com",
  "preferred_store": "Anand Jewels - Main Branch",
  "preferred_date_time": "2024-01-20 at 3:00 PM",
  "created_at": "2024-01-15T14:30:00"
}
```

### Get All Contact Enquiries
```bash
curl -X GET "http://localhost:8000/api/contact-enquiries" \
  -H "accept: application/json"
```

### Get All Contact Enquiries (Limited)
```bash
curl -X GET "http://localhost:8000/api/contact-enquiries?limit=10" \
  -H "accept: application/json"
```

### Get Specific Contact Enquiry
```bash
curl -X GET "http://localhost:8000/api/contact-enquiries/1" \
  -H "accept: application/json"
```

## Gold Rate APIs (Existing)

### Get Latest Rates
```bash
curl -X GET "http://localhost:8000/api/gold-rates/latest" \
  -H "accept: application/json"
```

### Get 7-Day History
```bash
curl -X GET "http://localhost:8000/api/gold-rates/history/7d" \
  -H "accept: application/json"
```

### Get History by Purity
```bash
curl -X GET "http://localhost:8000/api/gold-rates/history/24K?days=7" \
  -H "accept: application/json"
```

## JavaScript Examples

### Create Contact Enquiry with JavaScript
```javascript
const createEnquiry = async () => {
  const enquiryData = {
    name: "Jane Smith",
    phone_number: "+91 9876543211",
    email: "jane.smith@example.com",
    preferred_store: "Anand Jewels - City Center",
    preferred_date_time: "2024-01-22 at 4:30 PM"
  };

  try {
    const response = await fetch('http://localhost:8000/api/contact-enquiries', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(enquiryData)
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Enquiry created:', result);
    } else {
      console.error('Error:', response.statusText);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
};
```

### Get All Stores with JavaScript
```javascript
const getStores = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/stores');
    if (response.ok) {
      const stores = await response.json();
      console.log('Stores:', stores);
      return stores;
    }
  } catch (error) {
    console.error('Error fetching stores:', error);
  }
};
```

## Python Examples

### Using requests library
```python
import requests

# Get all stores
response = requests.get('http://localhost:8000/api/stores')
stores = response.json()
print(f"Found {len(stores)} stores")

# Create contact enquiry
enquiry_data = {
    "name": "Python User",
    "phone_number": "+91 9876543212",
    "email": "python@example.com",
    "preferred_store": "Anand Jewels - Main Branch",
    "preferred_date_time": "2024-01-25 at 11:00 AM"
}

response = requests.post(
    'http://localhost:8000/api/contact-enquiries',
    json=enquiry_data
)

if response.status_code == 200:
    enquiry = response.json()
    print(f"Created enquiry #{enquiry['id']}")
```

## Error Handling

### Invalid Store Name
When creating a contact enquiry with an invalid store name:
```json
{
  "detail": "Invalid store name. Available stores: Anand Jewels - Main Branch, Anand Jewels - City Center, Anand Jewels - Heritage Branch"
}
```

### Store Not Found
When requesting a non-existent store:
```json
{
  "detail": "Store not found"
}
```

### Validation Errors
When sending invalid data:
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

## API Documentation

Visit the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
