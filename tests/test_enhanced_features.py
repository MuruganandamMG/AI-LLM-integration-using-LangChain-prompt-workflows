import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

@pytest.mark.asyncio
async def test_enhanced_habit_lifecycle_and_exports():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        reg = await ac.post("/api/v1/auth/register", json={
            "email": "enhanced_user@example.com",
            "password": "Password123!",
            "full_name": "Enhanced User"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "enhanced_user@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Create habit
        create_resp = await ac.post("/api/v1/habits/", json={
            "title": "Deep Work Sprint",
            "description": "50 mins focused coding",
            "category": "Productivity",
            "frequency": "daily"
        }, headers=headers)
        assert create_resp.status_code == 201
        habit_id = create_resp.json()["id"]

        # 2. Update habit
        update_resp = await ac.put(f"/api/v1/habits/{habit_id}", json={
            "title": "Deep Work Sprint (Updated)",
            "frequency": "daily"
        }, headers=headers)
        assert update_resp.status_code == 200
        assert update_resp.json()["title"] == "Deep Work Sprint (Updated)"

        # 3. Export ICS
        ics_resp = await ac.get("/api/v1/habits/export/ics", headers=headers)
        assert ics_resp.status_code == 200
        assert "BEGIN:VCALENDAR" in ics_resp.text
        assert "Deep Work Sprint" in ics_resp.text

        # 4. Export CSV
        csv_resp = await ac.get("/api/v1/habits/export/csv", headers=headers)
        assert csv_resp.status_code == 200
        assert "Title,Category,Frequency" in csv_resp.text

        # 5. Delete habit
        del_resp = await ac.delete(f"/api/v1/habits/{habit_id}", headers=headers)
        assert del_resp.status_code == 204

@pytest.mark.asyncio
async def test_quote_and_focus_endpoints():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        reg = await ac.post("/api/v1/auth/register", json={
            "email": "focus_user@example.com",
            "password": "Password123!",
            "full_name": "Focus Hero"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "focus_user@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Daily quote
        quote_resp = await ac.get("/api/v1/reviews/quote?category=Productivity", headers=headers)
        assert quote_resp.status_code == 200
        assert "quote" in quote_resp.json()

        # Focus strategy
        focus_resp = await ac.post("/api/v1/analytics/focus-strategy", json={
            "task_title": "Build UI Dashboard",
            "duration_minutes": 25
        }, headers=headers)
        assert focus_resp.status_code == 200
        assert "priming_steps" in focus_resp.json()
