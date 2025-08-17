from typing import TypeVar, Generic, Optional, List, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import DeclarativeBase

T = TypeVar('T', bound=DeclarativeBase)

class BaseRepository(Generic[T]):
    def __init__(self, db:AsyncSession, model:Type[T]):
        self.db = db
        self.model = model

    async def create(self, **kwargs) -> T:
        """Create a new record."""
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
    
    async def get_by_id(self, id: int) -> Optional[T]:
        "Get record by ID."
        return self.db.get(self.model, id)

    async def get_all(self, limit: int = 20, offset: int = 0) -> List[T]:
        "Get all record with paginiation" 
        result = await self.db.execute(
            select(self.model).limit(limit).offset(offset)
        )
        return result.scalars().all()
    
    async def update(self, id: int, **kwargs) -> Optional[T]:
        """Update record by ID"""
        await self.db.execute(
            update(self.model).where(self.model.id == id).values(**kwargs)
        )
        await self.db.commit()
        return await self.get_by_id(id)

    async def delete(self, id:int) -> bool:
        """Delete rec
        ord by ID"""
        result = await self.db.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def exist(self, **filters) -> bool:
        """Check if record exist with filters"""
        query = select(self.db)
        for key, value in filters.items():
            query = query.where(getattr(self.model, key) == value)

        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None