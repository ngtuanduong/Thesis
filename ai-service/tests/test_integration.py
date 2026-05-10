"""
End-to-end integration test for the adaptive learning pipeline.

Tests the full cycle: submission update → all 4 layers → recommendations → knowledge state.
Requires a running database with seeded data (users, problems, concepts).

Run with: python -m pytest tests/test_integration.py -v
"""

import asyncio
import uuid

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import settings

SERVICE_KEY = settings.ai_service_key
HEADERS = {"x-service-key": SERVICE_KEY}

# Use the seeded student user (must exist in DB)
SEEDED_STUDENT_ID = "52d6fd7f-c5c0-4fcd-b586-17145bbff8d8"


@pytest_asyncio.fixture(scope="session")
async def client():
    """Create async test client. Rebinds DB engine to the test event loop."""
    import app.database as db_module
    db_module.engine = create_async_engine(settings.database_url, echo=False)
    db_module.async_session = async_sessionmaker(
        db_module.engine, class_=AsyncSession, expire_on_commit=False
    )

    from app.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    await db_module.engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def problem_id():
    """Get a valid problem ID from the database."""
    import app.database as db_module
    async with db_module.async_session() as session:
        result = await session.execute(
            text("SELECT problem_id FROM problem_concepts LIMIT 1")
        )
        row = result.first()
        return str(row[0]) if row else None


class TestHealthCheck:
    """Basic connectivity tests."""

    @pytest.mark.asyncio(scope="session")
    async def test_health(self, client):
        """Health endpoint should return ok."""
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


class TestAdaptivePipeline:
    """Full pipeline integration tests."""

    @pytest.mark.asyncio(scope="session")
    async def test_full_submission_cycle(self, client, problem_id):
        """Test: submit → update all layers → verify state changes."""
        if problem_id is None:
            pytest.skip("No problem-concept mappings in database")

        # 1. Get baseline knowledge state
        resp = await client.get(
            f"/adaptive/knowledge-state/{SEEDED_STUDENT_ID}",
            headers=HEADERS,
        )
        assert resp.status_code == 200

        # 2. Submit a correct answer
        resp = await client.post(
            "/adaptive/update",
            headers=HEADERS,
            json={
                "student_id": SEEDED_STUDENT_ID,
                "problem_id": problem_id,
                "is_correct": True,
                "attempt_number": 1,
                "time_spent_seconds": 120.0,
            },
        )
        assert resp.status_code == 200
        update_result = resp.json()

        # Verify all layers responded
        assert "bkt_update" in update_result
        assert "elo_update" in update_result
        assert "mab_update" in update_result
        assert "fsrs_update" in update_result

        # 3. Verify BKT updated
        if settings.enable_bkt:
            bkt = update_result["bkt_update"]
            assert "updates" in bkt
            if bkt["updates"]:
                primary = next(
                    (u for u in bkt["updates"] if u.get("is_primary")), None
                )
                if primary:
                    assert primary["p_mastery_after"] >= primary["p_mastery_before"]

        # 4. Verify Elo updated
        if settings.enable_elo:
            elo = update_result["elo_update"]
            assert "student_elo_after" in elo or "expected" in elo

        # 5. Verify FSRS updated
        if settings.enable_fsrs:
            fsrs = update_result["fsrs_update"]
            assert "state" in fsrs
            assert fsrs["reps"] >= 1

        # 6. Get updated knowledge state
        resp = await client.get(
            f"/adaptive/knowledge-state/{SEEDED_STUDENT_ID}",
            headers=HEADERS,
        )
        assert resp.status_code == 200
        updated_state = resp.json()
        assert "concepts" in updated_state
        assert "student_elo" in updated_state
        assert "review_queue" in updated_state
        assert "knowledge_graph" in updated_state

        # Verify knowledge graph structure
        kg = updated_state["knowledge_graph"]
        assert len(kg["nodes"]) > 0
        assert len(kg["edges"]) > 0

        # 7. Get recommendations
        resp = await client.get(
            f"/adaptive/recommend/{SEEDED_STUDENT_ID}",
            headers=HEADERS,
        )
        assert resp.status_code == 200
        recs = resp.json()
        assert "recommendations" in recs
        assert "knowledge_summary" in recs

    @pytest.mark.asyncio(scope="session")
    async def test_incorrect_submission(self, client, problem_id):
        """Test that incorrect submission also processes without error."""
        if problem_id is None:
            pytest.skip("No problem-concept mappings in database")

        resp = await client.post(
            "/adaptive/update",
            headers=HEADERS,
            json={
                "student_id": SEEDED_STUDENT_ID,
                "problem_id": problem_id,
                "is_correct": False,
                "attempt_number": 3,
                "time_spent_seconds": 300.0,
            },
        )
        assert resp.status_code == 200
        result = resp.json()
        assert "bkt_update" in result

    @pytest.mark.asyncio(scope="session")
    async def test_recommendations_return_problems(self, client):
        """Recommendations should return problem suggestions."""
        resp = await client.get(
            f"/adaptive/recommend/{SEEDED_STUDENT_ID}?limit=3",
            headers=HEADERS,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)

    @pytest.mark.asyncio(scope="session")
    async def test_review_queue(self, client):
        """Review queue should return structured data."""
        resp = await client.get(
            f"/adaptive/review-queue/{SEEDED_STUDENT_ID}",
            headers=HEADERS,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "due_now" in data
        assert "upcoming" in data


class TestKnowledgeTracing:
    """BKT endpoint integration tests."""

    @pytest.mark.asyncio(scope="session")
    async def test_get_state(self, client):
        """GET /kt/state should return knowledge states."""
        resp = await client.get(
            f"/kt/state/{SEEDED_STUDENT_ID}",
            headers=HEADERS,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert "states" in data or isinstance(data, list)

    @pytest.mark.asyncio(scope="session")
    async def test_predict(self, client, problem_id):
        """GET /kt/predict should return prediction."""
        if problem_id is None:
            pytest.skip("No problem mappings")

        resp = await client.get(
            f"/kt/predict/{SEEDED_STUDENT_ID}/{problem_id}",
            headers=HEADERS,
        )
        assert resp.status_code == 200


class TestEloEndpoints:
    """Elo rating endpoint integration tests."""

    @pytest.mark.asyncio(scope="session")
    async def test_get_student_elo(self, client):
        """GET /elo/student should return student rating."""
        resp = await client.get(
            f"/elo/student/{SEEDED_STUDENT_ID}",
            headers=HEADERS,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "rating" in data

    @pytest.mark.asyncio(scope="session")
    async def test_zpd(self, client):
        """GET /elo/zpd should return problems in zone of proximal development."""
        resp = await client.get(
            f"/elo/zpd/{SEEDED_STUDENT_ID}",
            headers=HEADERS,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "problems" in data or "zpd_problems" in data


class TestEvaluationEndpoints:
    """Evaluation/logging endpoint tests."""

    @pytest.mark.asyncio(scope="session")
    async def test_log_event(self, client):
        """POST /evaluation/log should store an event."""
        resp = await client.post(
            "/evaluation/log",
            headers=HEADERS,
            json={
                "user_id": SEEDED_STUDENT_ID,
                "event": "test_integration_event",
                "data": {"test": True},
            },
        )
        assert resp.status_code == 200

    @pytest.mark.asyncio(scope="session")
    async def test_experiment_stats(self, client):
        """GET /evaluation/stats should return statistics."""
        resp = await client.get(
            "/evaluation/stats",
            headers=HEADERS,
        )
        assert resp.status_code == 200
        assert isinstance(resp.json(), dict)
