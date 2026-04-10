import uuid
from collections import defaultdict

from sentence_transformers import SentenceTransformer
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import Problem, Submission, SubmissionStatus


DIFFICULTY_WEIGHTS = {
    "EASY": 1.0,
    "MEDIUM": 2.0,
    "HARD": 3.0,
}

# Saturation cap: accumulated difficulty points needed for score = 1.0.
# ~5 medium problems (5 * 2.0 = 10.0) or ~3-4 hard problems before a skill
# is considered fully exercised by this heuristic.
# Note: the authoritative mastery metric is the BKT p_mastery from
# bkt_service.py / KnowledgeState. This score is kept only for legacy
# callers and as an auxiliary signal for embeddings.
SKILL_SATURATION_POINTS = 10.0


class ProfileService:
    def __init__(self, model: SentenceTransformer):
        self.model = model

    async def compute_profile(
        self,
        session: AsyncSession,
        user_id: str,
    ) -> list[dict]:
        # Convert string UUID to UUID object
        user_uuid = uuid.UUID(user_id)

        # Fetch accepted submissions with problem info
        result = await session.execute(
            select(Submission, Problem)
            .join(Problem, Submission.problem_id == Problem.id)
            .where(
                Submission.user_id == user_uuid,
                Submission.status == SubmissionStatus.ACCEPTED,
            )
        )
        rows = result.all()

        # Group by tags and compute weighted scores
        skill_scores: dict[str, float] = defaultdict(float)
        skill_counts: dict[str, int] = defaultdict(int)

        for submission, problem in rows:
            weight = DIFFICULTY_WEIGHTS.get(problem.difficulty.value, 1.0)
            tags = problem.tags or []
            if not tags:
                tags = ["general"]
            for tag in tags:
                skill_scores[tag] += weight
                skill_counts[tag] += 1

        # Normalize scores to a 0-1 range against a fixed saturation cap
        # (NOT against the max of the user's own scores — that produced
        # spurious 100% mastery from a single submission).
        for skill in skill_scores:
            skill_scores[skill] = round(
                min(skill_scores[skill] / SKILL_SATURATION_POINTS, 1.0),
                4,
            )

        # Generate embeddings for each skill and upsert
        skills = []
        for skill_name, score in skill_scores.items():
            embedding = self.model.encode(skill_name, normalize_embeddings=True).tolist()
            embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

            await session.execute(
                text("""
                    INSERT INTO skill_embeddings (id, "userId", "skillName", embedding, embedding_vec, score, "updatedAt")
                    VALUES (:id, :user_id, :skill_name, :embedding, :embedding_vec, :score, NOW())
                    ON CONFLICT ("userId", "skillName")
                    DO UPDATE SET embedding = :embedding, embedding_vec = :embedding_vec, score = :score, "updatedAt" = NOW()
                """),
                {
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "skill_name": skill_name,
                    "embedding": embedding,
                    "embedding_vec": embedding_str,
                    "score": score,
                },
            )
            skills.append({"skill_name": skill_name, "score": score})

        await session.commit()
        return skills
