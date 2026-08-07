import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_request_id_middleware():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/healthcheck")
        assert resp.status_code == 200
        assert "x-request-id" in resp.headers
        assert "x-process-time-ms" in resp.headers
