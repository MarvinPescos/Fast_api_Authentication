import time 
from .metrics import REQUEST_COUNT, REQUEST_DURATION

async def metrics_middleware(request, call_next):
    """Middleware to collect metrics for all requests"""
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    # Record request count
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    ).inc()

    return response