from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

async def get_metrics():
    """Prometheus metric endpoint"""
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )