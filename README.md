# Django Twilio SMS API

A Django REST API for sending SMS messages using Twilio.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   - Create a `.env` file in the project root (copy from `.env.example`):
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with your Twilio credentials:
     ```
     TWILIO_ACCOUNT_SID=your-account-sid-here
     TWILIO_AUTH_TOKEN=your-auth-token-here
     TWILIO_MESSAGING_SERVICE_SID=your-messaging-service-sid-here
     ```
   - **Important:** Never commit the `.env` file to version control!

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Send SMS

**Endpoint:** `POST /api/send-sms/`

**Request Body:**
```json
{
    "to": "+18777804236",
    "body": "Your message here"
}
```

**Success Response (200 OK):**
```json
{
    "success": true,
    "message": "SMS sent successfully",
    "data": {
        "message_sid": "SM...",
        "to": "+18777804236",
        "body": "Your message here",
        "status": "queued",
        "date_created": "2025-10-03T..."
    }
}
```

**Error Response (400 Bad Request):**
```json
{
    "success": false,
    "errors": {
        "to": ["Phone number must include country code (e.g., +1 for US)"],
        "body": ["Message body cannot be empty"]
    }
}
```

## Testing with cURL

```bash
curl -X POST http://localhost:8000/api/send-sms/ \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+18777804236",
    "body": "Hello from Django Twilio API!"
  }'
```

## Testing with Postman

1. Method: `POST`
2. URL: `http://localhost:8000/api/send-sms/`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
       "to": "+18777804236",
       "body": "Test message"
   }
   ```

## Project Structure

```
django-twilio-project/
├── core/                      # Main app
│   ├── serializers.py         # Request validation
│   ├── views.py               # API endpoints
│   └── urls.py                # App URL routing
├── twilioapi/                 # Project settings
│   ├── settings.py            # Django settings & Twilio config
│   └── urls.py                # Main URL routing
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

## Notes

- Phone numbers must include country code (e.g., `+1` for US)
- Message body max length: 1600 characters
- The API uses Twilio's Messaging Service for sending SMS

