import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

@pytest.mark.asyncio
async def test_habit_schedule_fields_and_focus_logging():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        reg = await ac.post("/api/v1/auth/register", json={
            "email": "v2_tester@example.com",
            "password": "Password123!",
            "full_name": "V2 Master"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "v2_tester@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Create habit with time_of_day, estimated_minutes, priority
        habit_resp = await ac.post("/api/v1/habits/", json={
            "title": "Morning Cold Plunge & Journal",
            "description": "5 mins plunge followed by 10 mins stream of consciousness",
            "category": "Health",
            "frequency": "daily",
            "time_of_day": "morning",
            "estimated_minutes": 15,
            "priority": "high"
        }, headers=headers)
        assert habit_resp.status_code == 201
        data = habit_resp.json()
        assert data["time_of_day"] == "morning"
        assert data["estimated_minutes"] == 15
        assert data["priority"] == "high"

        # 2. Log Focus Session
        focus_resp = await ac.post("/api/v1/analytics/focus-session", json={
            "task_title": "Deep Architecture Refactor",
            "duration_minutes": 50,
            "soundscape": "binaural"
        }, headers=headers)
        assert focus_resp.status_code == 201
        assert focus_resp.json()["duration_minutes"] == 50

        # 3. Retrieve Focus Sessions
        list_focus = await ac.get("/api/v1/analytics/focus-sessions", headers=headers)
        assert list_focus.status_code == 200
        assert list_focus.json()["total_sessions"] >= 1
        assert list_focus.json()["total_focus_minutes"] >= 50
