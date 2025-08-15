import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from app.core import settings
from app.errors import DatabaseConnectionError


DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async def check_db() -> str:
    try:
         async with engine.connect() as conn:
              await conn.execute(text("SELECT 1"))
              print("✅` Database is connected")
    except Exception as e:
         print(f"Failed to connect{str(e)}")
         raise DatabaseConnectionError("Failed to connect to Databse")
    
if __name__ == "__main__":
     asyncio.run(check_db())

