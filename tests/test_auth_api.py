import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

@pytest.mark.asyncio
async def test_auth_register_and_login():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register
        reg_resp = await ac.post("/api/v1/auth/register", json={
            "email": "user@example.com",
            "password": "Password123!",
            "full_name": "Test User"
        })
        assert reg_resp.status_code == 201
        data = reg_resp.json()
        assert data["email"] == "user@example.com"

        # Login
        login_resp = await ac.post("/api/v1/auth/login", data={
            "username": "user@example.com",
            "password": "Password123!"
        })
        assert login_resp.status_code == 200
        token_data = login_resp.json()
        assert "access_token" in token_data

        # Me
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        me_resp = await ac.get("/api/v1/auth/me", headers=headers)
        assert me_resp.status_code == 200
        assert me_resp.json()["email"] == "user@example.com"
