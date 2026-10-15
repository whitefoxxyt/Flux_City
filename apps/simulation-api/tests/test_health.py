import asyncio

import httpx

from fluxcity_simulation_api.main import app


def test_health_returns_up() -> None:
    async def request_health() -> None:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            response = await client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "UP"}

    asyncio.run(request_health())
