from __future__ import annotations

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from backend.app.config import get_settings
from backend.app.database import async_session_factory, init_db
from backend.app.main import app
from backend.app.seed import seed_data

settings = get_settings()


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db():
    """Initializes and seeds test database before tests execute."""
    await init_db()
    async with async_session_factory() as session:
        await seed_data(session)


@pytest.mark.asyncio
async def test_healthcheck():
    """Verifies service health check response."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_get_venues():
    """Verifies palatial venues are seeded and returned."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/venues")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        slugs = [v["slug"] for v in data]
        assert "the-royal-palace" in slugs
        assert "the-royal-banquet" in slugs


@pytest.mark.asyncio
async def test_get_blog_posts():
    """Verifies authentic WordPress blog posts are accessible."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/blog")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        assert any("Marriage Hall in Delhi" in b["title"] for b in data)


@pytest.mark.asyncio
async def test_availability_check():
    """Verifies date and capacity recommender engine."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/availability/check",
            params={"date": "2026-11-20", "guests": "grand"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["date"] == "2026-11-20"
        assert "The Royal Palace" in data["recommended_venue"]


@pytest.mark.asyncio
async def test_submit_inquiry():
    """Verifies family inquiry lead capture and validation."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "full_name": "Kavita Kapoor",
            "phone": "+919876543210",
            "email": "kavita.kapoor@example.com",
            "celebration_type": "Grand Wedding & Reception",
            "estimated_guests": "Medium (300 – 600 Guests)",
            "preferred_date": "2026-12-18",
            "message": "Step-free ramp required for senior family members."
        }
        response = await client.post("/api/v1/inquiries", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] > 0
        assert data["full_name"] == "Kavita Kapoor"
        assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_admin_auth_and_protected_stats():
    """Verifies admin JWT token issuance and stats access."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Login
        login_res = await client.post(
            "/api/v1/auth/login",
            json={
                "username": settings.DEFAULT_ADMIN_USERNAME,
                "password": settings.DEFAULT_ADMIN_PASSWORD
            }
        )
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        assert token is not None

        # Fetch stats with token
        headers = {"Authorization": f"Bearer {token}"}
        stats_res = await client.get("/api/v1/inquiries/stats", headers=headers)
        assert stats_res.status_code == 200
        stats = stats_res.json()
        assert "pending" in stats
        assert stats["total"] >= 1
