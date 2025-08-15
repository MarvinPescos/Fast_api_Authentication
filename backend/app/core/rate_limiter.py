from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core import settings
import os

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.REDIS_URL
)

def get_user_key(request):
    """Extract user_id from request for user_based rate-limiting"""
    try:
        if hasattr(request, 'path_params'):
            user_id = request.path_params.get('user_id')
            if user_id:
                return f"user_{user_id}"
        return get_remote_address(request)
    except:
        return get_remote_address(request)

resend_verification_limiter =limiter.limit("5/hour", key_func=get_user_key)


