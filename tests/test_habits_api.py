import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

@pytest.mark.asyncio
async def test_habits_crud_and_logging():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register user & get token
        reg = await ac.post("/api/v1/auth/register", json={
            "email": "habituser@example.com",
            "password": "Password123!",
            "full_name": "Habit User"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "habituser@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create Habit
        create_resp = await ac.post("/api/v1/habits/", json={
            "title": "Daily Meditation",
            "description": "10 minutes of mindfulness",
            "category": "Mindfulness",
            "frequency": "daily"
        }, headers=headers)
        assert create_resp.status_code == 201
        habit_id = create_resp.json()["id"]

        # List Habits
        list_resp = await ac.get("/api/v1/habits/", headers=headers)
        assert list_resp.status_code == 200
        assert len(list_resp.json()) == 1

        # Log Habit Completion
        log_resp = await ac.post(f"/api/v1/habits/{habit_id}/log", json={
            "notes": "Felt very calm",
            "mood_score": 5
        }, headers=headers)
        assert log_resp.status_code == 201
        assert log_resp.json()["notes"] == "Felt very calm"
