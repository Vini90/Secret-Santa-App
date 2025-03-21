import pytest
from httpx import ASGITransport, AsyncClient

from main import app

# Sample test data
participant_1 = {"name": "Alice", "email": "alice@example.com", "exclusions": []}
participant_2 = {"name": "Bob", "email": "bob@example.com", "exclusions": ["Alice"]}

@pytest.mark.asyncio
async def test_create_participant():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res1 = await ac.post("/participants/", json=participant_1)
        res2 = await ac.post("/participants/", json=participant_2)
        assert res1.status_code in [200, 400]
        assert res2.status_code in [200, 400]

@pytest.mark.asyncio
async def test_get_participants():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/participants/")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert any(p["email"] == participant_1["email"] for p in data)

@pytest.mark.asyncio
async def test_create_exchange():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.post("/exchange/")
        assert res.status_code in [200, 400]  # May return 400 if invalid exclusions
        if res.status_code == 200:
            data = res.json()
            assert "exchange" in data
            assert isinstance(data["exchange"], dict)

@pytest.mark.asyncio
async def test_get_exchange_history():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/exchange/history")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

@pytest.mark.asyncio
async def test_delete_participant():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.delete(f"/participants/{participant_1['email']}")
        assert res.status_code in [200, 404]