import asyncio
from app.database import AsyncSessionLocal, init_db
from app.models.user import User
from app.models.habit import Habit
from app.core.security import get_password_hash

async def seed():
    await init_db()
    async with AsyncSessionLocal() as session:
        demo_user = User(
            email="demo@example.com",
            full_name="Demo User",
            hashed_password=get_password_hash("DemoPass123!")
        )
        session.add(demo_user)
        await session.commit()
        await session.refresh(demo_user)
        
        h1 = Habit(user_id=demo_user.id, title="Morning Run", category="Fitness", frequency="daily")
        h2 = Habit(user_id=demo_user.id, title="Read Tech Articles", category="Learning", frequency="daily")
        session.add_all([h1, h2])
        await session.commit()
        print("Demo database populated with user demo@example.com")

if __name__ == "__main__":
    asyncio.run(seed())
