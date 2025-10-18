import httpx
import random
import structlog
from datetime import datetime, time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional, List, Tuple
from fastapi import HTTPException, status

from app.activities.cat_facts.models import CatFactSubscription
from app.activities.cat_facts.schemas import (
    CatFactSubscriptionCreate,
    CatFactSubscriptionUpdate,
    CatFactResponse
)
from app.activities.cat_facts.templates import (
    get_cat_fact_html_template,
    get_cat_fact_text_template,
    get_welcome_subscription_html,
    get_welcome_subscription_text
)
from app.users import User
from app.email.service import EmailService
from app.core import settings

logger = structlog.get_logger(__name__)


# Cat Facts API and fallback data
CAT_FACT_API = "https://catfact.ninja/fact"

FALLBACK_FACTS = [
    "Cats have five toes on their front paws, but only four toes on their back paws.",
    "A cat's purr vibrates at a frequency that promotes bone healing.",
    "Cats can rotate their ears 180 degrees.",
    "A group of cats is called a 'clowder'.",
    "Cats sleep 12-16 hours per day.",
    "A cat's sense of smell is 14 times stronger than humans.",
    "Cats have over 20 vocalizations, including the purr, meow, and chirp.",
    "A cat's whiskers are roughly as wide as their body.",
    "Cats can jump up to six times their length.",
    "The first cat in space was a French cat named Felicette in 1963."
]


class CatFactsService:
    """Service for managing cat facts subscriptions and sending emails"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.email_service = EmailService()

    async def fetch_cat_fact(self) -> CatFactResponse:
        """Fetch a random cat fact from API or use fallback"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(CAT_FACT_API, timeout=10)
                if response.status_code == 200:
                    fact_data = response.json()
                    fact = fact_data.get('fact')
                    if fact:
                        logger.info("cat_fact_fetched_from_api")
                        return CatFactResponse(
                            fact=fact,
                            source="api",
                            length=len(fact),
                            fetched_at=datetime.utcnow()
                        )
        except Exception as e:
            logger.warning("cat_fact_api_failed", error=str(e))

        # Fallback to local facts
        fact = random.choice(FALLBACK_FACTS)
        logger.info("cat_fact_using_fallback")
        return CatFactResponse(
            fact=fact,
            source="fallback",
            length=len(fact),
            fetched_at=datetime.utcnow()
        )

    async def get_subscription(self, user_id: int) -> Optional[CatFactSubscription]:
        """Get user's cat fact subscription"""
        result = await self.db.execute(
            select(CatFactSubscription).where(CatFactSubscription.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_subscription(
        self,
        user_id: int,
        subscription_data: CatFactSubscriptionCreate
    ) -> CatFactSubscription:
        """Create a new cat fact subscription for user"""
        try:
            # Check if subscription already exists
            existing = await self.get_subscription(user_id)
            if existing:
                if existing.is_active:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="User already subscribed to cat facts"
                    )
                else:
                    # Reactivate existing subscription
                    existing.is_active = True
                    existing.preferred_time = subscription_data.preferred_time
                    existing.timezone = subscription_data.timezone
                    await self.db.commit()
                    await self.db.refresh(existing)
                    logger.info("cat_fact_subscription_reactivated", user_id=user_id)
                    return existing

            # Create new subscription
            subscription = CatFactSubscription(
                user_id=user_id,
                is_active=True,
                preferred_time=subscription_data.preferred_time,
                timezone=subscription_data.timezone
            )

            self.db.add(subscription)
            await self.db.commit()
            await self.db.refresh(subscription)

            logger.info("cat_fact_subscription_created", user_id=user_id)

            # Send welcome email
            user = await self.db.get(User, user_id)
            if user:
                await self._send_welcome_email(user)

            return subscription

        except HTTPException:
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error("cat_fact_subscription_creation_failed", user_id=user_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create subscription"
            )

    async def update_subscription(
        self,
        user_id: int,
        update_data: CatFactSubscriptionUpdate
    ) -> CatFactSubscription:
        """Update user's subscription preferences"""
        try:
            subscription = await self.get_subscription(user_id)
            if not subscription:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subscription not found"
                )

            # Update fields
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(subscription, key, value)

            await self.db.commit()
            await self.db.refresh(subscription)

            logger.info("cat_fact_subscription_updated", user_id=user_id)
            return subscription

        except HTTPException:
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error("cat_fact_subscription_update_failed", user_id=user_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update subscription"
            )

    async def unsubscribe(self, user_id: int) -> bool:
        """Unsubscribe user from cat facts (soft delete)"""
        try:
            subscription = await self.get_subscription(user_id)
            if not subscription:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subscription not found"
                )

            subscription.is_active = False
            await self.db.commit()

            logger.info("cat_fact_unsubscribed", user_id=user_id)
            return True

        except HTTPException:
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error("cat_fact_unsubscribe_failed", user_id=user_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to unsubscribe"
            )

    async def get_active_subscriptions(self) -> List[CatFactSubscription]:
        """Get all active subscriptions for daily send"""
        result = await self.db.execute(
            select(CatFactSubscription)
            .where(CatFactSubscription.is_active == True)
        )
        return list(result.scalars().all())

    async def send_cat_fact_to_user(self, subscription: CatFactSubscription) -> Tuple[bool, str]:
        """Send a cat fact email to a specific user"""
        try:
            # Get user
            user = await self.db.get(User, subscription.user_id)
            if not user:
                return False, f"User {subscription.user_id} not found"

            # Fetch cat fact
            cat_fact_response = await self.fetch_cat_fact()
            cat_fact = cat_fact_response.fact

            # Prepare email content
            current_date = datetime.now().strftime('%A, %B %d, %Y')
            user_name = user.username or user.full_name or "Friend"

            html_content = get_cat_fact_html_template(cat_fact, current_date, user_name)
            text_content = get_cat_fact_text_template(cat_fact, current_date, user_name)

            subject = f"🐱 Daily Cat Fact - {datetime.now().strftime('%B %d, %Y')}"

            # Send email via Brevo
            email_sent = await self.email_service.send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )

            if email_sent:
                # Update subscription stats
                subscription.last_sent_at = datetime.utcnow()
                subscription.total_sent += 1
                await self.db.commit()

                logger.info("cat_fact_sent", user_id=user.id, email=user.email)
                return True, f"Sent to {user.email}"
            else:
                logger.warning("cat_fact_send_failed", user_id=user.id, email=user.email)
                return False, f"Failed to send to {user.email}"

        except Exception as e:
            logger.error("cat_fact_send_error", user_id=subscription.user_id, error=str(e))
            return False, str(e)

    async def send_daily_cat_facts(self) -> Tuple[int, int, int, List[str], str]:
        """
        Send cat facts to all active subscribers
        Returns: (success_count, fail_count, total_subscribers, details, execution_time)
        """
        start_time = datetime.utcnow()
        logger.info("cat_facts_daily_send_started")

        subscriptions = await self.get_active_subscriptions()
        total_subscribers = len(subscriptions)
        success_count = 0
        fail_count = 0
        details = []

        for subscription in subscriptions:
            success, message = await self.send_cat_fact_to_user(subscription)
            if success:
                success_count += 1
            else:
                fail_count += 1
            details.append(f"User {subscription.user_id}: {message}")

        end_time = datetime.utcnow()
        execution_time = str(end_time - start_time)

        logger.info(
            "cat_facts_daily_send_completed",
            total=total_subscribers,
            success=success_count,
            failed=fail_count,
            execution_time=execution_time
        )

        return success_count, fail_count, total_subscribers, details, execution_time

    async def _send_welcome_email(self, user: User) -> bool:
        """Send welcome email when user subscribes"""
        try:
            user_name = user.username or user.full_name or "Friend"
            html_content = get_welcome_subscription_html(user_name)
            text_content = get_welcome_subscription_text(user_name)
            subject = "🎉 Welcome to Daily Cat Facts!"

            return await self.email_service.send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
        except Exception as e:
            logger.warning("welcome_email_failed", user_id=user.id, error=str(e))
            return False
