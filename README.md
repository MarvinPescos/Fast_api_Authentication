# FastAPI Authentication System 🔐

A production-ready authentication system built with FastAPI. Provides secure user registration, email verification, login/logout, password reset, and comprehensive security features for modern web applications.

## 🚀 Features

### ✅ **Features**

- 🔐 **Complete Authentication System**
  - User registration with email verification
  - Secure login/logout with JWT tokens
  - Password reset via email
  - Rate limiting protection
- 📧 **Email Services**
  - SendGrid integration
  - HTML/Text email templates
  - Verification codes and reset tokens
- 🛡️ **Security & Monitoring**
  - Password hashing (bcrypt)
  - JWT token authentication
  - Rate limiting (Redis-based)
  - Error tracking (Sentry)
  - Metrics collection (Prometheus)
- 🗄️ **Database Infrastructure**
  - PostgreSQL with async SQLAlchemy
  - Alembic migrations
  - Industry-standard schema design
- 🏗️ **Production-Ready Foundation**
  - Clean architecture with service layers
  - Comprehensive error handling
  - Docker support
  - CORS configuration

## 🛠️ Prerequisites

- **Python 3.11+**
- **PostgreSQL 15+**
- **Redis 7+**
- **SendGrid Account** (for emails)
- **Sentry Account** (for error tracking)

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd fastapi-auth-system
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### 3. Database Setup with Docker (Recommended)

```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Verify containers are running
docker ps
```

### 4. Environment Configuration

Create `.env` file in the `backend/` directory:

```env
# Database Settings
DB_USER=postgres
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=auth_system_db

# JWT Settings
SECRET_KEY=your_super_secret_jwt_key_32_characters_minimum
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App Settings
APP_NAME=Auth System
DEBUG=False
FRONTEND_URL=http://localhost:3000

# Email Settings (SendGrid)
MAIL_FROM=your-verified-email@domain.com
MAIL_FROM_NAME=Auth System
SENDGRID_API_KEY=your_sendgrid_api_key

# Redis Settings
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_URL=redis://localhost:6379/0

# Monitoring
SENTRY_DSN=your_sentry_dsn_url

# Email Verification
EMAIL_VERIFICATION_CODE_EXPIRY_MINUTES=15
```

### 5. Database Migrations

```bash
# Run database migrations
alembic upgrade head
```

### 6. Start the Application

```bash
# Development server
uvicorn app.main:app --reload

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint                                | Description                    |
| ------ | --------------------------------------- | ------------------------------ |
| `POST` | `/balance_hub/auth/register`            | Register new user              |
| `POST` | `/balance_hub/auth/verify-email`        | Verify email with 6-digit code |
| `POST` | `/balance_hub/auth/resend-verification` | Resend verification email      |
| `POST` | `/balance_hub/auth/login`               | Login user                     |
| `POST` | `/balance_hub/auth/logout`              | Logout user                    |
| `PUT`  | `/balance_hub/auth/update-user`         | Update user profile            |
| `POST` | `/balance_hub/auth/password/forget`     | Request password reset         |
| `POST` | `/balance_hub/auth/password/reset`      | Reset password with token      |

### System Endpoints

| Method | Endpoint   | Description        |
| ------ | ---------- | ------------------ |
| `GET`  | `/`        | API info           |
| `GET`  | `/health`  | Health check       |
| `GET`  | `/metrics` | Prometheus metrics |

## 🔧 Development

### Project Structure

```
fastapi-auth-system/
├── backend/
│   ├── app/
│   │   ├── auth/              # Authentication endpoints & logic
│   │   ├── core/              # Core utilities (config, security, etc.)
│   │   ├── email/             # Email services
│   │   ├── email_verification/# Email verification logic
│   │   ├── errors/            # Custom exception classes
│   │   ├── monitoring/        # Metrics and monitoring
│   │   ├── repositories/      # Data access layer
│   │   ├── templates/         # Email templates
│   │   ├── users/             # User models and schemas
│   │   └── main.py            # FastAPI application
│   ├── alembic/               # Database migrations
│   ├── docker-compose.yml     # Docker services
│   └── requirements.txt       # Python dependencies
├── env/                       # Virtual environment
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

### Running Tests

```bash
# Install test dependencies (when tests are added)
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Check current migration
alembic current

# View migration history
alembic history
```

### Code Quality

```bash
# Format code
black app/

# Sort imports
isort app/

# Type checking
mypy app/
```

## 🔒 Security Features

- **Password Security**: bcrypt hashing with salt
- **JWT Tokens**: Secure authentication with HTTP-only cookies
- **Rate Limiting**: Protection against brute force attacks
- **CORS**: Properly configured for frontend integration
- **Input Validation**: Pydantic schema validation
- **SQL Injection Protection**: SQLAlchemy ORM
- **Email Security**: Separate tokens for different verification types

## 📊 Monitoring & Observability

- **Error Tracking**: Sentry integration for production error monitoring
- **Metrics**: Prometheus metrics collection
- **Logging**: Structured logging with contextual information
- **Health Checks**: Built-in health check endpoints

## 🐳 Docker Support

### Development

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Production Deployment

```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d
```

## 🚨 Troubleshooting

### Common Issues

**1. Database Connection Error**

```bash
# Check if PostgreSQL is running
docker ps
# Verify connection settings in .env file
```

**2. Email Not Sending**

- Verify SendGrid API key in `.env`
- Check sender email is verified in SendGrid
- Ensure SENDGRID_API_KEY has proper permissions

**3. JWT Token Issues**

- Ensure SECRET_KEY is at least 32 characters
- Check token expiration settings
- Verify CORS configuration for cookie handling

**4. Redis Connection Error**

```bash
# Check if Redis is running
docker ps
# Test Redis connection
redis-cli ping
```

## 🚀 Possible Enhancements

### Authentication Features

- [ ] **OAuth Integration**
  - [ ] Google OAuth
  - [ ] GitHub OAuth
  - [ ] Microsoft OAuth
- [ ] **Security Enhancements**
  - [ ] Two-factor authentication (2FA)
  - [ ] Account lockout after failed attempts
  - [ ] Login session management
  - [ ] Device tracking

### Admin Features

- [ ] **User Management**
  - [ ] Admin dashboard
  - [ ] User search and management
  - [ ] Role-based access control
  - [ ] Audit logging

### Developer Experience

- [ ] **Testing & Quality**
  - [ ] Comprehensive test suite
  - [ ] API documentation improvements
  - [ ] Performance monitoring
  - [ ] Load testing

### Integration Features

- [ ] **API Improvements**
  - [ ] GraphQL support
  - [ ] Webhook notifications
  - [ ] API rate limiting per user
  - [ ] Multiple API versions

---

**FastAPI Authentication System** - Production-ready user authentication for modern web applications! 🔐✨
