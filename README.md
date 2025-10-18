# Mini App

## Overview

A production-ready, enterprise-grade authentication system built with FastAPI and React. This application provides comprehensive user authentication and authorization capabilities, including secure registration, email verification, session management, and password recovery mechanisms.

## Quick Start

For those who want to get started immediately:

```bash
# Clone and navigate to project
git clone <repository-url>
cd Full-stack_Authentication/Fast_api_Authentication

# Backend setup
cd backend
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt

# Start services (requires Docker)
docker-compose up -d

# Configure environment (copy and edit .env)
cp env.example .env
# Edit .env with your credentials

# Run migrations
alembic upgrade head

# Start backend
uvicorn app.main:app --reload

# In a new terminal - Frontend setup
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173 for the frontend and http://localhost:8000/docs for API documentation.

## Architecture

This application follows a modern, scalable architecture with clear separation of concerns:

### Backend Architecture

- **API Layer**: FastAPI with RESTful endpoints
- **Service Layer**: Business logic and authentication services
- **Repository Layer**: Data access abstraction
- **Database Layer**: PostgreSQL with SQLAlchemy ORM (async)
- **Caching Layer**: Redis for rate limiting and session management
- **Email Service**: Brevo (formerly Sendinblue) integration
- **Monitoring**: Sentry for error tracking, Prometheus for metrics

### Frontend Architecture

- **UI Framework**: React 19 with TypeScript
- **State Management**: Zustand for global state
- **Routing**: React Router v7
- **Styling**: Tailwind CSS v4
- **Build Tool**: Vite for fast development and optimized production builds
- **Validation**: Zod schemas for type-safe data validation
- **HTTP Client**: Axios with interceptors

## Features

### Authentication and Authorization

- **User Registration**: Secure account creation with input validation
- **Email Verification**: Six-digit verification code system with expiration
- **User Login**: JWT-based authentication with HTTP-only cookies
- **User Logout**: Secure session termination
- **Password Reset**: Email-based password recovery with secure tokens
- **Profile Management**: User information update capabilities

### Security Features

- **Password Hashing**: bcrypt with automatic salt generation
- **JWT Authentication**: Stateless authentication with configurable expiration
- **Rate Limiting**: Redis-backed rate limiting to prevent brute force attacks
- **CORS Protection**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic schemas for request/response validation
- **SQL Injection Protection**: ORM-based queries with parameterization
- **Email Security**: Separate verification tokens for different operations

### Infrastructure Features

- **Database Migrations**: Alembic for version-controlled schema changes
- **Docker Support**: Containerized PostgreSQL and Redis services
- **Health Checks**: System health monitoring endpoints
- **Error Tracking**: Sentry integration for production error monitoring
- **Metrics Collection**: Prometheus metrics for performance monitoring
- **Structured Logging**: Comprehensive logging with contextual information

### OAuth Integration (Not yet implemented)

- Database schema includes OAuth provider fields (Google, Facebook)
- OAuth service foundation implemented (currently commented out)
- Ready for third-party authentication integration

## Technology Stack

### Backend Technologies

| Technology        | Version | Purpose                                 |
| ----------------- | ------- | --------------------------------------- |
| Python            | 3.11+   | Primary programming language            |
| FastAPI           | Latest  | Web framework for building APIs         |
| SQLAlchemy        | Latest  | Async ORM for database operations       |
| PostgreSQL        | 15+     | Primary database                        |
| Redis             | 7+      | Caching and rate limiting               |
| Alembic           | Latest  | Database migration tool                 |
| Pydantic          | Latest  | Data validation and settings management |
| Passlib/Bcrypt    | Latest  | Password hashing                        |
| Python-JOSE       | Latest  | JWT token generation and validation     |
| Brevo SDK         | Latest  | Email service integration               |
| Sentry SDK        | Latest  | Error tracking                          |
| Prometheus Client | Latest  | Metrics collection                      |
| SlowAPI           | Latest  | Rate limiting                           |
| Structlog         | Latest  | Structured logging                      |

### Frontend Technologies

| Technology   | Version | Purpose                     |
| ------------ | ------- | --------------------------- |
| React        | 19.1.1  | UI library                  |
| TypeScript   | 5.8.3   | Type-safe JavaScript        |
| Vite         | 7.1.6   | Build tool and dev server   |
| React Router | 7.9.1   | Client-side routing         |
| Zustand      | 5.0.8   | State management            |
| Axios        | 1.12.2  | HTTP client                 |
| Zod          | 4.1.11  | Schema validation           |
| Tailwind CSS | 4.1.13  | Utility-first CSS framework |

## Prerequisites

Before installation, ensure you have the following installed:

- **Python**: Version 3.11 or higher
- **Node.js**: Version 18 or higher
- **npm**: Version 9 or higher
- **PostgreSQL**: Version 15 or higher
- **Redis**: Version 7 or higher
- **Docker** (optional but recommended): Latest stable version
- **Git**: For version control

### External Services Required

- **Brevo Account**: For email service (free tier available)
- **Sentry Account**: For error tracking (free tier available)

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd Full-stack_Authentication/Fast_api_Authentication
```

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv env

# Activate virtual environment
# On Linux/macOS:
source env/bin/activate
# On Windows:
# env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Configuration

### Backend Environment Configuration

Create a `.env` file in the `backend/` directory with the following configuration:

```env
# Database Configuration
DB_USER=postgres
DB_PASS=your_secure_database_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fullstack_auth

# JWT Configuration (minimum 32 characters for SECRET_KEY)
SECRET_KEY=your_super_secret_jwt_key_minimum_32_characters_replace_this_immediately
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
APP_NAME=Full-Stack Authentication
DEBUG=False
FRONTEND_URL=http://localhost:5173

# Email Service Configuration (Brevo)
MAIL_FROM=your-verified-email@yourdomain.com
MAIL_FROM_NAME=Full-Stack Authentication
BREVO_API_KEY=your_brevo_api_key_here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_URL=redis://localhost:6379/0

# Monitoring Configuration
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# Email Verification Settings
EMAIL_VERIFICATION_CODE_EXPIRY_MINUTES=15

# OAuth Configuration (optional, for future use)
# FACEBOOK_CLIENT_ID=your_facebook_app_id
# FACEBOOK_CLIENT_SECRET=your_facebook_app_secret
# FACEBOOK_REDIRECT_URI=http://localhost:8000/auth/facebook/callback
```

### Frontend Configuration

Update the API base URL in `frontend/src/shared/utils/constant.ts`:

```typescript
export const API_BASE_URL =
  "http://localhost:8000/fullstack_authentication/auth";
```

## Database Setup

### Using Docker (Recommended)

```bash
# Navigate to backend directory
cd backend

# Start PostgreSQL and Redis containers
docker-compose up -d

# Verify containers are running
docker ps

# Expected output should show:
# - fullstack_auth_db (PostgreSQL)
# - fullstack_auth_redis (Redis)
```

### Manual Setup (Alternative)

If you prefer manual installation:

1. **Install PostgreSQL 15+**

   ```bash
   # Create database
   createdb fullstack_auth
   ```

2. **Install Redis 7+**
   ```bash
   # Start Redis server
   redis-server
   ```

### Run Database Migrations

```bash
# Ensure you're in the backend directory with virtual environment activated
cd backend
source env/bin/activate  # On Windows: env\Scripts\activate

# Run migrations
alembic upgrade head

# Verify migration status
alembic current
```

## Running the Application

### Development Mode

**Backend:**

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source env/bin/activate  # On Windows: env\Scripts\activate

# Start development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at:

- **API Base**: http://localhost:8000
- **Interactive API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Metrics**: http://localhost:8000/metrics

**Frontend:**

```bash
# Navigate to frontend directory
cd frontend

# Start development server
npm run dev
```

The frontend will be available at: http://localhost:5173

### Production Mode

**Backend:**

```bash
# Use production-ready ASGI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## API Documentation

### Authentication Endpoints

| Method | Endpoint                                             | Description                           | Rate Limit |
| ------ | ---------------------------------------------------- | ------------------------------------- | ---------- |
| `POST` | `/fullstack_authentication/auth/register`            | Register new user account             | 5/minute   |
| `POST` | `/fullstack_authentication/auth/verify-email`        | Verify email with 6-digit code        | None       |
| `POST` | `/fullstack_authentication/auth/resend-verification` | Resend verification email             | Custom     |
| `POST` | `/fullstack_authentication/auth/login`               | Authenticate user and receive JWT     | 10/minute  |
| `POST` | `/fullstack_authentication/auth/logout`              | Terminate user session                | None       |
| `PUT`  | `/fullstack_authentication/auth/update-user`         | Update user profile information       | None       |
| `POST` | `/fullstack_authentication/auth/password/forget`     | Request password reset email          | 5/minute   |
| `POST` | `/fullstack_authentication/auth/password/reset`      | Reset password with verification code | 10/hour    |

### System Endpoints

| Method | Endpoint   | Description                 |
| ------ | ---------- | --------------------------- |
| `GET`  | `/`        | API information and version |
| `GET`  | `/health`  | Application health status   |
| `GET`  | `/metrics` | Prometheus metrics endpoint |

### Request/Response Examples

**User Registration:**

```bash
POST /fullstack_authentication/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john.doe@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Email Verification:**

```bash
POST /fullstack_authentication/auth/verify-email
Content-Type: application/json

{
  "user_id": 1,
  "code": "123456"
}
```

**User Login:**

```bash
POST /fullstack_authentication/auth/login
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "SecurePassword123!"
}
```

## Project Structure

```
Fast_api_Authentication/
├── backend/
│   ├── alembic/                      # Database migrations
│   │   ├── versions/                 # Migration scripts
│   │   └── env.py                    # Alembic configuration
│   ├── app/
│   │   ├── auth/                     # Authentication module
│   │   │   ├── router.py             # API endpoints
│   │   │   ├── service.py            # Business logic
│   │   │   ├── schemas.py            # Request/response models
│   │   │   ├── dependencies.py       # Dependency injection
│   │   │   └── oauth_service.py      # OAuth implementation (prepared)
│   │   ├── core/                     # Core utilities
│   │   │   ├── config.py             # Configuration management
│   │   │   ├── database.py           # Database connection
│   │   │   ├── security.py           # Security utilities
│   │   │   ├── middleware.py         # Custom middleware
│   │   │   ├── rate_limiter.py       # Rate limiting
│   │   │   ├── metrics.py            # Metrics collection
│   │   │   └── logging_setup.py      # Logging configuration
│   │   ├── email/                    # Email service
│   │   │   └── service.py            # Email sending logic
│   │   ├── email_verification/       # Email verification module
│   │   │   ├── services.py           # Verification logic
│   │   │   └── schemas.py            # Verification models
│   │   ├── errors/                   # Custom exceptions
│   │   │   ├── authentication_errors.py
│   │   │   ├── authorization_errors.py
│   │   │   ├── database_errors.py
│   │   │   ├── validation_errors.py
│   │   │   └── system_errors.py
│   │   ├── monitoring/               # Observability
│   │   │   └── prometheus.py         # Prometheus metrics
│   │   ├── repositories/             # Data access layer
│   │   │   ├── base.py               # Base repository
│   │   │   └── user_repositories.py  # User data access
│   │   ├── templates/                # Email templates
│   │   │   └── emails/
│   │   │       ├── verification.html
│   │   │       ├── verification.txt
│   │   │       ├── reset_password.html
│   │   │       └── reset_password.txt
│   │   ├── users/                    # User module
│   │   │   ├── models.py             # SQLAlchemy models
│   │   │   └── schemas.py            # Pydantic schemas
│   │   └── main.py                   # Application entry point
│   ├── docker-compose.yml            # Docker services configuration
│   ├── requirements.txt              # Python dependencies
│   ├── alembic.ini                   # Alembic configuration
│   └── env.example                   # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── features/                 # Feature-based organization
│   │   │   ├── auth/                 # Authentication feature
│   │   │   │   ├── hooks/            # Custom React hooks
│   │   │   │   ├── pages/            # Page components
│   │   │   │   ├── schemas/          # Zod validation schemas
│   │   │   │   ├── services/         # API service calls
│   │   │   │   ├── store/            # Zustand state management
│   │   │   │   └── types/            # TypeScript types
│   │   │   └── users/                # User feature
│   │   │       └── schemas/
│   │   ├── shared/                   # Shared resources
│   │   │   ├── components/           # Reusable components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Form.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   └── LoadingSpinner.tsx
│   │   │   ├── hooks/                # Shared hooks
│   │   │   ├── services/             # API client
│   │   │   ├── store/                # Global state
│   │   │   ├── types/                # Shared types
│   │   │   └── utils/                # Utility functions
│   │   ├── App.tsx                   # Root component
│   │   ├── main.tsx                  # Application entry
│   │   └── index.css                 # Global styles
│   ├── package.json                  # Node dependencies
│   ├── tsconfig.json                 # TypeScript configuration
│   ├── vite.config.ts                # Vite configuration
│   └── eslint.config.js              # ESLint configuration
└── README.md                         # This file
```

## Security Features

### Authentication Security

- **Password Hashing**: Utilizes bcrypt with automatic salt generation and configurable work factor
- **JWT Tokens**: Stateless authentication with configurable expiration times
- **HTTP-only Cookies**: Prevents XSS attacks by storing tokens in HTTP-only cookies
- **Secure Cookie Flags**: SameSite and Secure flags for CSRF protection

### Application Security

- **Rate Limiting**: Redis-backed rate limiting on authentication endpoints
- **Input Validation**: Comprehensive Pydantic schema validation on all inputs
- **SQL Injection Protection**: ORM-based queries with automatic parameterization
- **CORS Configuration**: Strict cross-origin resource sharing policies
- **Error Handling**: Generic error messages to prevent information leakage

### Data Security

- **Email Verification**: Separate verification codes for registration and password reset
- **Token Expiration**: Time-limited verification codes and reset tokens
- **Password Policies**: Configurable password strength requirements
- **Account Status**: Active/inactive status with email verification requirement

## Monitoring and Observability

### Error Tracking

- **Sentry Integration**: Real-time error tracking and alerting
- **Error Context**: Automatic capture of request context and user information
- **Stack Traces**: Full stack traces for debugging
- **Release Tracking**: Version-based error tracking

### Performance Monitoring

- **Prometheus Metrics**: Standard application metrics
- **Custom Metrics**: Request duration, error rates, active users
- **Health Checks**: Database and Redis connectivity monitoring

### Logging

- **Structured Logging**: JSON-formatted logs with context
- **Log Levels**: Configurable logging levels for different environments
- **Request Tracking**: Automatic logging of all API requests
- **Error Logging**: Comprehensive error information capture

## Development Guidelines

### Database Migrations

```bash
# Create new migration after model changes
alembic revision --autogenerate -m "Description of changes"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# Check current migration version
alembic current
```

### Code Quality

**Backend:**

```bash
# Format code with Black
black app/

# Sort imports
isort app/

# Type checking
mypy app/

# Run linters
flake8 app/
```

**Frontend:**

```bash
# Lint code
npm run lint

# Type checking
npx tsc --noEmit

# Build check
npm run build
```

### Testing

```bash
# Backend testing (when test suite is implemented)
pytest tests/ -v --cov=app

# Frontend testing (when test suite is implemented)
npm run test
```

### Git Workflow

1. Create feature branch from `main`
2. Make changes with descriptive commits
3. Run linters and formatters
4. Test changes locally
5. Create pull request with detailed description
6. Address code review feedback
7. Merge after approval

## Troubleshooting

### Database Connection Issues

**Problem**: Cannot connect to PostgreSQL database

**Solutions**:

```bash
# Check if PostgreSQL container is running
docker ps | grep postgres

# View PostgreSQL logs
docker logs fullstack_auth_db

# Restart PostgreSQL container
docker-compose restart postgres

# Verify connection settings in .env file
cat .env | grep DB_
```

### Redis Connection Issues

**Problem**: Redis connection errors or rate limiting not working

**Solutions**:

```bash
# Check if Redis container is running
docker ps | grep redis

# Test Redis connection
redis-cli ping
# Expected output: PONG

# View Redis logs
docker logs fullstack_auth_redis

# Restart Redis container
docker-compose restart redis
```

### Email Sending Issues

**Problem**: Verification emails not being sent

**Solutions**:

1. Verify Brevo API key is correct in `.env`
2. Ensure sender email is verified in Brevo dashboard
3. Check API key has proper permissions
4. Review Brevo API limits (free tier has sending limits)
5. Check application logs for email service errors

### JWT Token Issues

**Problem**: Authentication failures or token validation errors

**Solutions**:

1. Ensure `SECRET_KEY` is at least 32 characters
2. Verify `SECRET_KEY` matches between backend instances
3. Check token expiration settings
4. Verify CORS configuration allows credentials
5. Ensure cookies are being set with correct flags

### Migration Issues

**Problem**: Alembic migration failures

**Solutions**:

```bash
# Check current database state
alembic current

# View pending migrations
alembic history

# If migrations are out of sync, stamp current version
alembic stamp head

# For development, you can drop database and recreate
# WARNING: This will delete all data
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

### Frontend Build Issues

**Problem**: Vite build or development server errors

**Solutions**:

```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite

# Check Node.js version
node --version  # Should be 18+

# Update dependencies (if needed)
npm update
```

### CORS Issues

**Problem**: CORS errors when frontend calls backend

**Solutions**:

1. Verify `FRONTEND_URL` in backend `.env` matches frontend URL
2. Check `ALLOWED_ORIGINS` includes frontend URL
3. Ensure frontend is running on expected port (5173)
4. Verify credentials are included in frontend API calls
5. Check browser console for specific CORS error details

## Deployment

### Production Deployment Checklist

Before deploying to production, ensure the following:

**Environment Configuration:**

- [ ] Set `DEBUG=False` in backend `.env`
- [ ] Use strong, unique `SECRET_KEY` (minimum 32 characters)
- [ ] Configure production database credentials
- [ ] Set up production Redis instance
- [ ] Configure production email service
- [ ] Set up Sentry for error tracking

**Security:**

- [ ] Enable HTTPS/SSL certificates
- [ ] Update `ALLOWED_ORIGINS` to production URLs only
- [ ] Configure firewall rules
- [ ] Set secure cookie flags
- [ ] Review and update CORS settings
- [ ] Enable rate limiting

**Infrastructure:**

- [ ] Set up database backups
- [ ] Configure log aggregation
- [ ] Set up monitoring and alerts
- [ ] Configure auto-scaling (if needed)
- [ ] Set up CDN for static assets

### Docker Deployment

```bash
# Build production images
docker build -t fullstack-auth-backend:latest ./backend
docker build -t fullstack-auth-frontend:latest ./frontend

# Run with docker-compose (production)
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables for Production

Ensure all sensitive credentials are stored securely using environment variables or secrets management services (AWS Secrets Manager, Google Secret Manager, HashiCorp Vault, etc.).

## Contributing

We welcome contributions from the community. Please follow these guidelines:

### How to Contribute

1. **Fork the Repository**

   ```bash
   git clone https://github.com/yourusername/fullstack-authentication.git
   cd fullstack-authentication
   ```

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**

   - Follow the existing code style
   - Write clear, descriptive commit messages
   - Add comments where necessary
   - Update documentation as needed

4. **Test Your Changes**

   ```bash
   # Backend tests
   pytest tests/ -v

   # Frontend tests
   npm run test

   # Run linters
   black app/  # Backend
   npm run lint  # Frontend
   ```

5. **Submit a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all tests pass
   - Wait for code review

### Coding Standards

**Backend (Python):**

- Follow PEP 8 style guidelines
- Use type hints where applicable
- Write docstrings for functions and classes
- Maximum line length: 88 characters (Black default)

**Frontend (TypeScript):**

- Follow ESLint configuration
- Use TypeScript strict mode
- Write meaningful component and function names
- Use functional components with hooks

### Commit Message Guidelines

Follow the conventional commits specification:

```
feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting changes
refactor: code refactoring
test: adding tests
chore: maintenance tasks
```

### Code Review Process

1. All submissions require review from project maintainers
2. Address feedback promptly
3. Maintain professional and respectful communication
4. Be open to suggestions and alternative approaches

## Support

### Getting Help

If you encounter issues or have questions:

**Documentation:**

- Read this README thoroughly
- Check the [Troubleshooting](#troubleshooting) section
- Review API documentation at `/docs` endpoint

**Community Support:**

- Open an issue on GitHub with detailed information
- Include error messages, logs, and steps to reproduce
- Search existing issues before creating new ones

**Bug Reports:**

When reporting bugs, please include:

- Operating system and version
- Python and Node.js versions
- Full error message and stack trace
- Steps to reproduce the issue
- Expected vs actual behavior

**Feature Requests:**

For feature requests, please provide:

- Clear description of the proposed feature
- Use cases and benefits
- Any relevant examples or mockups

### Response Time

- Critical bugs: Within 24-48 hours
- General issues: Within 3-5 business days
- Feature requests: Reviewed during planning cycles

## Future Enhancements

### Planned Authentication Features

- **Multi-Factor Authentication (MFA)**: TOTP-based two-factor authentication
- **OAuth 2.0 Integration**: Google, Facebook, GitHub authentication
- **Social Login**: Complete OAuth provider implementations
- **Biometric Authentication**: WebAuthn/FIDO2 support
- **Session Management**: Active session tracking and management
- **Device Tracking**: Login history and device recognition
- **Account Recovery**: Alternative recovery methods

### Security Enhancements

- **Account Lockout**: Automatic lockout after failed login attempts
- **Password Policies**: Configurable complexity requirements
- **Password History**: Prevent password reuse
- **Security Questions**: Additional account recovery options
- **IP Whitelisting**: Restrict access by IP address
- **Audit Logging**: Comprehensive security event logging

### Administrative Features

- **Admin Dashboard**: User management interface
- **Role-Based Access Control (RBAC)**: Fine-grained permissions
- **User Search**: Advanced user filtering and search
- **Bulk Operations**: Batch user management operations
- **Analytics Dashboard**: User statistics and trends
- **Report Generation**: Security and usage reports

### Developer Experience

- **Comprehensive Test Suite**: Unit, integration, and E2E tests
- **API Versioning**: Support for multiple API versions
- **GraphQL Support**: Alternative API interface
- **Webhook System**: Event-driven integrations
- **API Rate Limiting**: Per-user rate limits
- **SDK Development**: Client libraries for popular languages
- **Documentation Portal**: Interactive API documentation

### Infrastructure Improvements

- **Horizontal Scaling**: Load balancer configuration
- **Caching Strategy**: Advanced caching with Redis
- **CDN Integration**: Static asset optimization
- **Database Replication**: Read replicas for scaling
- **Message Queue**: Asynchronous task processing
- **Microservices Architecture**: Service decomposition

## Acknowledgments

This project was built using excellent open-source technologies and tools:

**Backend Frameworks and Libraries:**

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and ORM
- [Alembic](https://alembic.sqlalchemy.org/) - Database migration tool
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation using Python type annotations
- [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server

**Frontend Frameworks and Libraries:**

- [React](https://reactjs.org/) - JavaScript library for building user interfaces
- [Vite](https://vitejs.dev/) - Next-generation frontend tooling
- [Zustand](https://zustand-demo.pmnd.rs/) - Lightweight state management
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Zod](https://zod.dev/) - TypeScript-first schema validation

**Infrastructure and Services:**

- [PostgreSQL](https://www.postgresql.org/) - Advanced open-source database
- [Redis](https://redis.io/) - In-memory data structure store
- [Docker](https://www.docker.com/) - Containerization platform
- [Brevo](https://www.brevo.com/) - Email marketing and transactional email service
- [Sentry](https://sentry.io/) - Application monitoring and error tracking
- [Prometheus](https://prometheus.io/) - Monitoring and alerting toolkit

---

**Developed with FastAPI, React, and modern web technologies.**

For questions, issues, or contributions, please refer to the project repository.
