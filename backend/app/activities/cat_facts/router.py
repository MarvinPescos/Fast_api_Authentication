from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.core import get_db
from app.auth.dependencies import get_current_user
from app.users import User
from app.activities.cat_facts.service import CatFactsService
from app.activities.cat_facts.schemas import (
    CatFactSubscriptionCreate,
    CatFactSubscriptionUpdate,
    CatFactSubscriptionResponse,
    SubscriptionStatusResponse,
    SubscribeResponse,
    UnsubscribeResponse,
    SendDailyRequest,
    SendDailyResponse,
    CatFactResponse
)
from app.core import settings

router = APIRouter()


def get_cat_facts_service(db: AsyncSession = Depends(get_db)) -> CatFactsService:
    """Dependency to get CatFactsService instance"""
    return CatFactsService(db)


@router.post(
    "/subscribe",
    response_model=SubscribeResponse,
    status_code=status.HTTP_201_CREATED,
    description="Subscribe to daily cat facts"
)
async def subscribe(
    subscription_data: CatFactSubscriptionCreate,
    current_user: User = Depends(get_current_user),
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """
    Subscribe authenticated user to daily cat facts
    User's timezone (default: UTC)
    """
    subscription = await service.create_subscription(
        user_id=current_user.id,
        subscription_data=subscription_data
    )

    return SubscribeResponse(
        success=True,
        message="Successfully subscribed to daily cat facts! 🐱",
        subscription=CatFactSubscriptionResponse.model_validate(subscription, from_attributes=True)
    )


@router.delete(
    "/unsubscribe",
    response_model=UnsubscribeResponse,
    status_code=status.HTTP_200_OK,
    description="Unsubscribe from daily cat facts"
)
async def unsubscribe(
    current_user: User = Depends(get_current_user),
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """
    Unsubscribe authenticated user from daily cat facts
    """
    await service.unsubscribe(current_user.id)

    return UnsubscribeResponse(
        success=True,
        message="Successfully unsubscribed from daily cat facts. We'll miss you! 😿",
        unsubscribed_at=datetime.utcnow()
    )


@router.get(
    "/status",
    response_model=SubscriptionStatusResponse,
    status_code=status.HTTP_200_OK,
    description="Check cat facts subscription status"
)
async def get_status(
    current_user: User = Depends(get_current_user),
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """
    Get authenticated user's cat facts subscription status
    """
    subscription = await service.get_subscription(current_user.id)

    if subscription and subscription.is_active:
        return SubscriptionStatusResponse(
            subscribed=True,
            subscription=CatFactSubscriptionResponse.model_validate(subscription, from_attributes=True),
            message=f"You're subscribed! Last sent: {subscription.last_sent_at or 'Never'}"
        )
    else:
        return SubscriptionStatusResponse(
            subscribed=False,
            subscription=None,
            message="You're not subscribed to daily cat facts"
        )


@router.put(
    "/preferences",
    response_model=CatFactSubscriptionResponse,
    status_code=status.HTTP_200_OK,
    description="Update cat facts preferences"
)
async def update_preferences(
    update_data: CatFactSubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """
    Update authenticated user's cat facts preferences
    """
    subscription = await service.update_subscription(
        user_id=current_user.id,
        update_data=update_data
    )

    return CatFactSubscriptionResponse.model_validate(subscription, from_attributes=True)


@router.get(
    "/random",
    response_model=CatFactResponse,
    status_code=status.HTTP_200_OK,
    description="Get a random cat fact (no authentication required)"
)
async def get_random_cat_fact(
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """
    Get a random cat fact from the API
    Public endpoint - no authentication required
    """
    return await service.fetch_cat_fact()


@router.post(
    "/send-daily",
    response_model=SendDailyResponse,
    status_code=status.HTTP_200_OK,
    description="Trigger daily cat facts send (for automated schedulers)"
)
async def send_daily(
    request_data: SendDailyRequest,
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """
    Trigger daily cat facts send to all active subscribers

    This endpoint is for automated schedulers (GitHub Actions, cron jobs, etc.)
    Requires API key authentication

    **Security**: Include api_key in request body
    """
    # Verify API key (use a secret from environment)
    # For now, we'll use the SECRET_KEY, but you should create a separate API_KEY
    if request_data.api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    success_count, fail_count, total_subscribers, details, execution_time = await service.send_daily_cat_facts()

    return SendDailyResponse(
        success=True,
        message=f"Daily cat facts sent! Success: {success_count}, Failed: {fail_count}",
        sent_count=success_count,
        failed_count=fail_count,
        total_subscribers=total_subscribers,
        execution_time=execution_time,
        details=details if fail_count > 0 else None
    )
