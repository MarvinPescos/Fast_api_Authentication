import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

from app.core import metrics_middleware  
from app.monitoring import get_metrics
from app.core import settings
from app.auth import router as auth_router


sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=0.1,
    debug=settings.DEBUG
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan management 
    """
    print(f"{settings.APP_NAME} starting up...")

    yield

    print(f"{settings.APP_NAME} shutting down...")



#FastApi instance
app = FastAPI(
    title=settings.APP_NAME,
    description="BalanceHub",
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

#COnfigure COrs
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-CSRF-Token",
        "Cache-Control",
        "Pragma"
    ],
    expose_headers=["Set-Cookie"],
)

#  metrics middleware
app.middleware("http")(metrics_middleware)

#  metrics endpoint
app.get("/metrics")(get_metrics)

#Include routers
app.include_router(auth_router, prefix="/fullstack_authentication/auth", tags=["Authentication"])

@app.get("/test-errors")
async def test_errors():
    """Test endpoint to trigger sentry error tracking - DEBUG only"""
    if not settings.DEBUG:
        raise HTTPException(status_code=404, detail="Not found")
    raise Exception("This is a test error for Sentry!")

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "BalanceHub",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy", 
        "service": settings.APP_NAME,
        "timestamp": datetime.utcnow().isoformat()
    }
