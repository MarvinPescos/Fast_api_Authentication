from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core import get_db, verify_access_token, get_token_from_cookie
from app.users import User
from app.auth.service import AuthService

async def get_current_user(
        request: Request,
        db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    This is the dependancy that clicks authentication
    """
    try:
        # get token from HTTP-only cookie
        token = get_token_from_cookie(request)

        payload = verify_access_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive"
            )

        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )

async def get_auth_service(db: AsyncSession = Depends(get_db)) ->  AuthService:
    """Dependency injection for AuthService."""
    return AuthService(db)