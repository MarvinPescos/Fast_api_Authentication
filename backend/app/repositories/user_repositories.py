from typing import  Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.repositories import BaseRepository
from app.users import User

class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        """User-speciic method"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_active_user(self, limit: int = 20, offset: int  = 0) -> List[User]:
        """Get all active user with pagination"""
        result = await self.db.execute(
            select(User).where(User.is_active == True).limit(limit).offset(offset)
        )
        return result.scalars().all()


