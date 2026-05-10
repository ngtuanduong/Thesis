from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class RecommendationService:
    async def get_recommendations(
        self,
        session: AsyncSession,
        user_id: str,
        limit: int = 10,
    ) -> list[dict]:
        # Get user's skill embeddings to build an aggregate profile vector
        skill_result = await session.execute(
            text("""
                SELECT embedding_vec
                FROM skill_embeddings
                WHERE "userId" = :user_id AND embedding_vec IS NOT NULL
            """),
            {"user_id": user_id},
        )
        skill_rows = skill_result.fetchall()

        if not skill_rows:
            # No skill profile yet — fall back to newest unsolved problems
            fallback = await session.execute(
                text("""
                    SELECT p.id, p.title, p.difficulty
                    FROM problems p
                    WHERE p.id NOT IN (
                        SELECT DISTINCT s."problemId" FROM submissions s
                        WHERE s."userId" = :user_id AND s.status = 'ACCEPTED'
                    )
                    ORDER BY p."createdAt" DESC
                    LIMIT :limit
                """),
                {"user_id": user_id, "limit": limit},
            )
            return [
                {"problem_id": str(r[0]), "title": r[1], "difficulty": str(r[2]), "score": 0.0}
                for r in fallback.fetchall()
            ]

        # Compute average user profile vector via SQL
        # Then find closest problem embeddings via cosine distance
        result = await session.execute(
            text("""
                WITH user_profile AS (
                    SELECT AVG(embedding_vec) AS profile_vec
                    FROM skill_embeddings
                    WHERE "userId" = :user_id AND embedding_vec IS NOT NULL
                )
                SELECT p.id, p.title, p.difficulty,
                       1 - (pe.embedding_vec <=> up.profile_vec) AS similarity
                FROM problem_embeddings pe
                JOIN problems p ON p.id = pe."problemId"
                CROSS JOIN user_profile up
                WHERE p.id NOT IN (
                    SELECT DISTINCT s."problemId" FROM submissions s
                    WHERE s."userId" = :user_id AND s.status = 'ACCEPTED'
                )
                AND pe.embedding_vec IS NOT NULL
                ORDER BY pe.embedding_vec <=> up.profile_vec ASC
                LIMIT :limit
            """),
            {"user_id": user_id, "limit": limit},
        )
        return [
            {
                "problem_id": str(r[0]),
                "title": r[1],
                "difficulty": str(r[2]),
                "score": round(float(r[3]), 4),
            }
            for r in result.fetchall()
        ]
