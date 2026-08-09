import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_gamification_profile():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register user
        await ac.post("/api/v1/auth/register", json={
            "email": "gamer@example.com",
            "password": "Password123!",
            "full_name": "Gamer User"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "gamer@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Check gamification stats
        resp = await ac.get("/api/v1/gamification/profile", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["level"] >= 1
        assert "badges" in data
        assert len(data["badges"]) == 4
