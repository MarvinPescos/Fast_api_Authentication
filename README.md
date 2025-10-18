# Full-Stack Authentication Application

A comprehensive full-stack web application demonstrating modern authentication patterns, built with FastAPI (Python) backend and React (TypeScript) frontend. This project showcases various authentication methods, security features, and interactive activities.

## Features

### Authentication & Security

- **User Registration & Email Verification** - Complete signup flow with email verification
- **JWT-based Authentication** - Secure token-based authentication with HTTP-only cookies
- **Two-Factor Authentication (2FA)** - TOTP-based 2FA using PyOTP
- **OAuth Integration** - Facebook and Google OAuth login
- **Password Reset** - Secure password reset via email
- **Rate Limiting** - Protection against brute force attacks
- **Session Management** - Secure session handling with Redis

### Interactive Activities

- **Trivia Game** - Interactive trivia questions using Open Trivia Database API
- **Cipher Tools** - Atbash, Caesar, and Vigenère cipher implementations
- **QR Code Generator** - Generate QR codes for any text
- **Joke Cipher QR** - Combined workflow: fetch joke → cipher → generate QR code
- **Campus Building Rater** - Rate and review campus buildings
- **Cat Facts Subscription** - Daily cat facts email subscription service

### Technical Features

- **Modern UI** - Built with React, TypeScript, and Tailwind CSS
- **Database Migrations** - Alembic for database schema management
- **Email Service** - Brevo (Sendinblue) integration for transactional emails
- **Caching** - Redis-based caching for improved performance
- **API Documentation** - Auto-generated OpenAPI/Swagger documentation

## Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **Alembic** - Database migrations
- **Pydantic** - Data validation and serialization
- **PyOTP** - Two-factor authentication
- **Brevo API** - Email service

### Frontend

- **React 19** - Frontend framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Zustand** - State management
- **Axios** - HTTP client
- **Zod** - Schema validation

## Prerequisites

Before running this application, ensure you have:

- **Python 3.13+** installed
- **Node.js 18+** and npm installed
- **PostgreSQL 15+** running locally or via Docker
- **Redis** running locally or via Docker
- **Git** for version control

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Full-stack_Authentication/Fast_api_Authentication
```

### 2. Backend Setup

#### Install Dependencies

```bash
cd backend
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

#### Environment Configuration

```bash
cp env.example .env
```

Edit `.env` file with your configuration:

```env
# Database Settings
DB_USER=postgres
DB_PASS=your_database_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=MiniApp_testDB

# JWT Settings (must be 32+ characters)
SECRET_KEY=your_super_secret_jwt_key_32_characters_minimum_replace_this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App Settings
APP_NAME=Mini App
DEBUG=True
FRONTEND_URL=http://localhost:5173

# Email Settings (Get API key from Brevo)
MAIL_FROM=your-verified-email@domain.com
MAIL_FROM_NAME=Mini App
BREVO_API_KEY=xkeysib-your_brevo_api_key

# Redis Settings
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_URL=redis://localhost:6379/0

# Monitoring (Get DSN from Sentry.io)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# OAuth Settings (Optional)
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_REDIRECT_URI=http://localhost:8000/auth/facebook/callback

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# External API URLs
OPENTDB_API_URL=https://opentdb.com/api.php
JOKE_API_URL=https://v2.jokeapi.dev/joke/Any
CAT_FACT_API=https://catfact.ninja/fact
```

#### Database Setup

```bash
# Start PostgreSQL and Redis using Docker Compose
docker-compose up -d

# Run database migrations
alembic upgrade head
```

#### Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Start Development Server

```bash
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## Docker Setup (Alternative)

If you prefer to run everything with Docker:

```bash
# Start database services
docker-compose up -d

# Backend (in separate terminal)
cd backend
source env/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in separate terminal)
cd frontend
npm run dev
```

## API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The API includes comprehensive documentation with:

- Request/response schemas
- Authentication requirements
- Example requests
- Interactive testing interface

## Authentication Flow

### 1. User Registration

```
POST /fullstack_authentication/auth/register
```

- Creates user account
- Sends verification email
- Returns success message

### 2. Email Verification

```
POST /fullstack_authentication/auth/verify-email
```

- Verifies email with 6-digit code
- Activates user account

### 3. Login

```
POST /fullstack_authentication/auth/login
```

- Authenticates user
- Returns JWT token in HTTP-only cookie
- Supports 2FA if enabled

### 4. Protected Routes

All activity endpoints require authentication:

```
GET /fullstack_authentication/activities/trivia
POST /fullstack_authentication/activities/cipher/atbash
POST /fullstack_authentication/activities/qr_generator/generate
```

## Available Activities

### Trivia Game

- Fetch random trivia questions
- Multiple categories and difficulty levels
- Real-time scoring

### Cipher Tools

- **Atbash**: Reverse alphabet cipher
- **Caesar**: Shift-based cipher with configurable shift
- **Vigenère**: Keyword-based polyalphabetic cipher

### QR Code Generator

- Generate QR codes for any text
- Base64 encoded PNG output
- Customizable size and error correction

### Joke Cipher QR

- Combined workflow: fetch joke → apply cipher → generate QR
- Multiple cipher options
- Single API call for complete process

### Campus Building Rater

- Rate campus buildings
- Leave reviews and comments
- View average ratings

### Cat Facts Subscription

- Subscribe to daily cat facts
- Email delivery at preferred times
- Unsubscribe functionality

## Development

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Frontend Development

```bash
# Run linting
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

### Backend Development

```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Run tests (if available)
pytest

# Check code formatting
black .
isort .
```

## Project Structure

```
Fast_api_Authentication/
├── backend/
│   ├── app/
│   │   ├── activities/          # Feature modules
│   │   │   ├── cat_facts/       # Cat facts subscription
│   │   │   ├── ciphers/         # Cipher tools
│   │   │   ├── joke_cipher_qr/ # Combined workflow
│   │   │   ├── qr_generator/   # QR code generation
│   │   │   ├── trivia/         # Trivia game
│   │   │   └── campus_building_rater/ # Building ratings
│   │   ├── auth/               # Authentication
│   │   ├── core/               # Core utilities
│   │   ├── email/              # Email services
│   │   ├── users/              # User management
│   │   └── main.py             # FastAPI app
│   ├── alembic/               # Database migrations
│   ├── requirements.txt       # Python dependencies
│   └── docker-compose.yml     # Database services
└── frontend/
    ├── src/
    │   ├── features/           # Feature modules
    │   ├── shared/             # Shared components
    │   └── App.tsx             # Main app component
    ├── package.json            # Node dependencies
    └── vite.config.ts          # Vite configuration
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**

   - Ensure PostgreSQL is running
   - Check database credentials in `.env`
   - Verify database exists

2. **Redis Connection Error**

   - Ensure Redis is running
   - Check Redis configuration in `.env`

3. **Email Not Sending**

   - Verify Brevo API key
   - Check sender email is verified
   - Ensure email service is properly configured

4. **Frontend Build Errors**

   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility

5. **CORS Issues**
   - Verify `FRONTEND_URL` in backend `.env`
   - Check `ALLOWED_ORIGINS` configuration

### Logs and Debugging

- **Backend logs**: Check terminal output for detailed error messages
- **Frontend logs**: Check browser developer console
- **Database logs**: Check PostgreSQL logs
- **Redis logs**: Check Redis logs

## Environment Variables Reference

| Variable           | Description                | Required | Default                  |
| ------------------ | -------------------------- | -------- | ------------------------ |
| `DB_USER`          | Database username          | Yes      | -                        |
| `DB_PASS`          | Database password          | Yes      | -                        |
| `DB_HOST`          | Database host              | No       | localhost                |
| `DB_PORT`          | Database port              | No       | 5432                     |
| `DB_NAME`          | Database name              | Yes      | -                        |
| `SECRET_KEY`       | JWT secret key (32+ chars) | Yes      | -                        |
| `BREVO_API_KEY`    | Email service API key      | Yes      | -                        |
| `MAIL_FROM`        | Verified sender email      | Yes      | -                        |
| `REDIS_URL`        | Redis connection URL       | No       | redis://localhost:6379/0 |
| `SENTRY_DSN`       | Error monitoring DSN       | Yes      | -                        |
| `FACEBOOK_APP_ID`  | Facebook OAuth app ID      | No       | -                        |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID     | No       | -                        |

## Contributing

This is a school project demonstrating full-stack development concepts. Key areas of focus:

1. **Security**: Authentication, authorization, and data protection
2. **Modern Architecture**: Clean separation of concerns
3. **API Design**: RESTful endpoints with proper documentation
4. **Frontend Integration**: React with TypeScript and modern tooling
5. **Database Design**: Proper schema design and migrations
6. **Error Handling**: Comprehensive error handling and logging

## License

This project is created for educational purposes as part of a school assignment.

## Learning Objectives

This project demonstrates:

- **Full-Stack Development**: Complete web application with frontend and backend
- **Authentication Patterns**: JWT, OAuth, 2FA, email verification
- **Modern Web Technologies**: FastAPI, React, TypeScript, Tailwind CSS
- **Database Management**: PostgreSQL, SQLAlchemy, Alembic migrations
- **Security Best Practices**: Password hashing, rate limiting, CORS
- **API Design**: RESTful APIs with comprehensive documentation
- **State Management**: Frontend state management with Zustand
- **Email Services**: Transactional email integration
- **Development Workflow**: Modern development tools and practices

---

**Note**: This is a demonstration project for educational purposes. Ensure you have proper API keys and configurations for production use.
