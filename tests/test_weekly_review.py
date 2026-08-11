import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_weekly_review_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post("/api/v1/auth/register", json={
            "email": "reviewer@example.com",
            "password": "Password123!",
            "full_name": "Review User"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "reviewer@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        resp = await ac.post("/api/v1/reviews/weekly", headers=headers)
        assert resp.status_code == 201
        data = resp.json()
        assert "overall_sentiment" in data
        assert "next_week_smart_goals" in data
        assert len(data["next_week_smart_goals"]) >= 1
