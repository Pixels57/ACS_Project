# Backend - Course Registration System

Monolithic FastAPI backend with intentional security vulnerabilities.

## Setup

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the application:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── main.py              # Main application entry point
├── database.py          # Database configuration
├── requirements.txt     # Python dependencies
├── models/              # SQLAlchemy models
│   ├── user.py
│   ├── course.py
│   ├── enrollment.py
│   └── audit.py
└── routes/              # API routes
    ├── auth.py          # Authentication (VULNERABLE: Broken Auth)
    ├── courses.py       # Courses (VULNERABLE: SQL Injection)
    ├── enrollments.py   # Enrollments (VULNERABLE: CSRF)
    ├── admin.py         # Admin operations
    └── audit.py         # Audit logs (VULNERABLE: Access Control)
```

## Security Vulnerabilities

⚠️ **This application contains intentional vulnerabilities:**

1. **SQL Injection** - `/api/v1/courses?filter=` parameter
2. **Broken Authentication** - Weak password hashing (MD5), no rate limiting
3. **CSRF** - `/api/v1/enrollments` lacks CSRF token validation
4. **Access Control** - Audit logs accessible without proper authorization

## Development

Run with auto-reload:
```bash
uvicorn main:app --reload
```

Run tests:
```bash
pytest
```

