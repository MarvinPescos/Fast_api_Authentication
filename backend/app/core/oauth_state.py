import secrets
from redis.asyncio import Redis
from typing import Optional

class OauthStateManager:
    """Manages oauth state tokens using Redis"""

    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379):
        self.redis_host = redis_host
        self.redis_port = redis_port

    async def _get_redis(self) -> Redis:
        """Create Redis Connection"""
        return Redis(
            host=self.redis_host,
            port=self.redis_port,
            decode_responses=True
        )

    async def create_state(self, ttl: int = 600) -> str:
        """
        Create and store a new OAuth State token

        Args:
            ttl: Time to live in seconds (default 10 minutes)

        Returns:
            The generate state token
        """
        state = secrets.token_urlsafe(32)

        redis = await self._get_redis()
        await redis.setex(f"oauth_state: {state}", ttl, "pending")
        await redis.close()

        return state

    async def validate_state(self, state: str) -> bool:
        """
        Validate and consume on OAuth state token

        Args:
            State: The state token to validate

        Returns:
            True if valid, False otherwise
        """
        redis = await self._get_redis()

        stored_state = await redis.get(f"oauth_state: {state}")

        if stored_state:
            await redis.delete(f"oauth_state:{state}")
            await redis.close()
            return True

        await redis.close()
        return False

oauth_state_manager = OauthStateManager()
