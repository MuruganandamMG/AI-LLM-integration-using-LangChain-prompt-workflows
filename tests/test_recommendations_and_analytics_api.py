import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

@pytest.mark.asyncio
async def test_recommendations_and_analytics_endpoints():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register user & get token
        await ac.post("/api/v1/auth/register", json={
            "email": "aiperson@example.com",
            "password": "Password123!",
            "full_name": "AI Tester"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "aiperson@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Generate Recommendation
        rec_resp = await ac.post("/api/v1/recommendations/generate", headers=headers)
        assert rec_resp.status_code == 201
        assert "title" in rec_resp.json()

        # Get Analytics Summary
        sum_resp = await ac.get("/api/v1/analytics/summary", headers=headers)
        assert sum_resp.status_code == 200
        assert "completion_rate" in sum_resp.json()

        # Generate Analytics Report
        rep_resp = await ac.post("/api/v1/analytics/generate-report", headers=headers)
        assert rep_resp.status_code == 201
        assert "ai_summary" in rep_resp.json()
