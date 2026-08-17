import pytest
from app.database import AsyncSessionLocal, init_db, Base, engine
from sqlalchemy import text

@pytest.mark.asyncio
async def test_database_connection():
    await init_db()
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
