from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response, HTTPException, Request
from app.core import settings

async def get_metrics(request: Request):
    """Prometheus metric endpoint - internal use only"""
    # Simple protection: only allow in DEBUG mode or from localhost
    client_host = request.client.host if request.client else "unknown"
    
    if not settings.DEBUG and client_host not in ["127.0.0.1", "::1", "localhost"]:
        raise HTTPException(status_code=404, detail="Not found")
    
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )