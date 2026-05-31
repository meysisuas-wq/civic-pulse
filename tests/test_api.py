import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestHealthEndpoints:
    async def test_root_endpoint(self, client: AsyncClient):
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "civic-pulse"

    async def test_api_root(self, client: AsyncClient):
        response = await client.get("/api/v1/")
        assert response.status_code == 200
        assert response.json()["version"] == "v1"

@pytest.mark.asyncio
class TestCitizenEndpoints:
    async def test_register_validation(self, client: AsyncClient):
        response = await client.post("/api/v1/citizens/register", json={"citizen_id": "123", "email": "bad"})
        assert response.status_code == 422

    async def test_login_missing(self, client: AsyncClient):
        response = await client.post("/api/v1/citizens/login", json={})
        assert response.status_code == 422

@pytest.mark.asyncio
class TestServiceEndpoints:
    async def test_list_services(self, client: AsyncClient):
        response = await client.get("/api/v1/services")
        assert response.status_code == 501

    async def test_get_stats(self, client: AsyncClient):
        response = await client.get("/api/v1/stats")
        assert response.status_code == 200
        assert "total_requests" in response.json()
