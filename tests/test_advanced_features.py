import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

@pytest.mark.asyncio
async def test_coach_chat_endpoint():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        reg = await ac.post("/api/v1/auth/register", json={
            "email": "chat_tester@example.com",
            "password": "Password123!",
            "full_name": "Chat Master"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "chat_tester@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Chat with coach
        chat_resp = await ac.post("/api/v1/coach/chat", json={
            "message": "How do I overcome morning procrastination?"
        }, headers=headers)
        assert chat_resp.status_code == 200
        assert "response" in chat_resp.json()
        assert len(chat_resp.json()["response"]) > 20

@pytest.mark.asyncio
async def test_gamification_quests_flow():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        reg = await ac.post("/api/v1/auth/register", json={
            "email": "quest_tester@example.com",
            "password": "Password123!",
            "full_name": "Quest Hero"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "quest_tester@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # List quests
        quests_resp = await ac.get("/api/v1/gamification/quests", headers=headers)
        assert quests_resp.status_code == 200
        quests = quests_resp.json()
        assert len(quests) >= 3
        assert quests[0]["id"] == "q1"

        # Create habit & log completion
        habit_resp = await ac.post("/api/v1/habits/", json={
            "title": "Morning Stretch",
            "category": "Health",
            "frequency": "daily"
        }, headers=headers)
        habit_id = habit_resp.json()["id"]

        await ac.post(f"/api/v1/habits/{habit_id}/log", json={
            "mood_score": 5,
            "notes": "Great energy"
        }, headers=headers)

        # Claim quest
        claim_resp = await ac.post("/api/v1/gamification/quests/q1/claim", headers=headers)
        assert claim_resp.status_code == 200
        assert claim_resp.json()["status"] == "claimed"

@pytest.mark.asyncio
async def test_mood_trends_endpoint():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        reg = await ac.post("/api/v1/auth/register", json={
            "email": "mood_tester@example.com",
            "password": "Password123!",
            "full_name": "Mood Analyzer"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "mood_tester@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        mood_resp = await ac.get("/api/v1/analytics/mood-trends", headers=headers)
        assert mood_resp.status_code == 200
        assert "summary" in mood_resp.json()
        assert "category_averages" in mood_resp.json()
