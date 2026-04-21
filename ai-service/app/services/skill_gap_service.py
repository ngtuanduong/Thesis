from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class SkillGapService:
    async def analyze(
        self,
        session: AsyncSession,
        user_id: str,
    ) -> list[dict]:
        # Get all unique concept names as the "ideal" skill set
        all_tags_result = await session.execute(
            text("""
                SELECT DISTINCT c.name AS tag
                FROM concepts c
                INNER JOIN problem_concepts pc ON pc.concept_id = c.id
                ORDER BY tag
            """)
        )
        all_tags = [r[0] for r in all_tags_result.fetchall()]

        if not all_tags:
            return []

        # Get user's current skill scores
        user_skills_result = await session.execute(
            text("""
                SELECT "skillName", score
                FROM skill_embeddings
                WHERE "userId" = :user_id
            """),
            {"user_id": user_id},
        )
        user_skills = {r[0]: float(r[1]) for r in user_skills_result.fetchall()}

        # Target score is 1.0 for all skills; gap = target - current
        gaps = []
        for tag in all_tags:
            current = user_skills.get(tag, 0.0)
            target = 1.0
            gap = round(target - current, 4)
            if gap > 0:
                gaps.append({
                    "skill_name": tag,
                    "current_score": current,
                    "target_score": target,
                    "gap": gap,
                })

        # Sort by largest gap first
        gaps.sort(key=lambda x: x["gap"], reverse=True)
        return gaps
