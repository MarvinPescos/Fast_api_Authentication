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
from app.auth.two_factor_router import router as two_factor_router
from app.oauth import router as oauth_router
from app.activities.trivia import router as opentdb_router
from app.activities.ciphers import router as cipher_router
from app.activities.qr_generator import router as qr_router
from app.activities.joke_cipher_qr import router as joke_router
from app.activities.campus_building_rater import router as building_rater
from app.activities.cat_facts import router as cat_facts_router

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
    description="Mini App",
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
app.include_router(two_factor_router, prefix="/fullstack_authentication/auth", tags=["Two-Factor Authentication"])
app.include_router(oauth_router, prefix="/fullstack_authentication/auth", tags=["OAuth"])
app.include_router(opentdb_router, prefix="/fullstack_authentication/activities/trivia", tags=["Activities - Trivia"])
app.include_router(cipher_router, prefix="/fullstack_authentication/activities/cipher", tags=["Activities - Ciphers"])
app.include_router(qr_router, prefix="/fullstack_authentication/activities/qr_generator", tags=["Activities - QR Generator"])
app.include_router(joke_router, prefix="/fullstack_authentication/activities/joke_cipher_qr", tags=["Activities - Joke Api"])
app.include_router(building_rater, prefix="/fullstack_authentication/activities/campus_building_rater", tags=["Activities - Building rater"])
app.include_router(cat_facts_router, prefix="/fullstack_authentication/activities/cat-facts", tags=["Activities - Cat Facts"])

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
