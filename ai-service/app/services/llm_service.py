"""
LLM Feedback Service — Layer 5: Hint Generation

Uses knowledge graph context + student state for Socratic hints.
Supports OpenAI API (GPT-4o-mini) with rate limiting.
Falls back gracefully if LLM is unavailable.
"""

import asyncio
import logging
import time
from collections import deque

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.tables import (
    Concept,
    KnowledgeGraphEdge,
    KnowledgeState,
    Problem,
    ProblemConcept,
)

logger = logging.getLogger(__name__)

# Rate limiter: sliding window
_request_timestamps: deque[float] = deque()


def _check_rate_limit() -> bool:
    """Returns True if request is allowed under rate limit."""
    now = time.time()
    window = 60.0  # 1 minute window
    while _request_timestamps and _request_timestamps[0] < now - window:
        _request_timestamps.popleft()
    if len(_request_timestamps) >= settings.llm_rate_limit_per_minute:
        return False
    _request_timestamps.append(now)
    return True


SYSTEM_PROMPT = """You are a Socratic programming tutor for a university Python course. Your role is to guide students toward understanding WITHOUT giving direct answers.

Rules:
1. NEVER provide complete solutions or direct code answers
2. Ask guiding questions that lead the student to the answer
3. Point out the specific concept they need to understand
4. Give small, incremental hints that build understanding
5. Reference prerequisite concepts when the student seems to lack foundational knowledge
6. Use encouraging language
7. Keep responses concise (2-4 sentences per hint)
8. If the student's code has a specific bug, describe the TYPE of error without showing the fix"""


async def _build_context(
    session: AsyncSession,
    student_id: str,
    problem_id: str,
) -> dict:
    """Build rich context from knowledge graph + student state."""
    # Get problem info
    prob_result = await session.execute(
        select(Problem).where(Problem.id == problem_id)
    )
    problem = prob_result.scalar_one_or_none()
    if not problem:
        return {"problem": None, "concepts": [], "student_mastery": {}}

    # Get concepts for this problem
    pc_result = await session.execute(
        select(ProblemConcept, Concept)
        .join(Concept, ProblemConcept.concept_id == Concept.id)
        .where(ProblemConcept.problem_id == problem_id)
    )
    concept_rows = pc_result.all()
    concepts = []
    concept_ids = []
    for pc, concept in concept_rows:
        concepts.append({
            "name": concept.display_name,
            "topic": concept.topic_group,
            "tier": concept.difficulty_tier,
            "is_primary": pc.is_primary,
        })
        concept_ids.append(concept.id)

    # Get prerequisites of these concepts
    prereq_result = await session.execute(
        select(KnowledgeGraphEdge, Concept)
        .join(Concept, KnowledgeGraphEdge.from_concept_id == Concept.id)
        .where(KnowledgeGraphEdge.to_concept_id.in_(concept_ids))
    )
    prereq_rows = prereq_result.all()
    prerequisites = [
        {"name": concept.display_name, "topic": concept.topic_group}
        for _, concept in prereq_rows
    ]

    # Get student's mastery of relevant concepts
    ks_result = await session.execute(
        select(KnowledgeState).where(
            KnowledgeState.student_id == student_id,
            KnowledgeState.concept_id.in_(concept_ids),
        )
    )
    student_states = ks_result.scalars().all()
    mastery_map = {}
    for ks in student_states:
        matching = [c for c in concept_rows if c[1].id == ks.concept_id]
        if matching:
            mastery_map[matching[0][1].display_name] = {
                "mastery": round(ks.p_mastery, 2),
                "attempts": ks.n_attempts,
                "correct": ks.n_correct,
            }

    return {
        "problem": {
            "title": problem.title,
            "description": problem.description[:500],
            "difficulty": problem.difficulty,
        },
        "concepts": concepts,
        "prerequisites": prerequisites,
        "student_mastery": mastery_map,
    }


def _build_hint_prompt(
    context: dict,
    student_code: str,
    error_message: str | None,
    hint_level: int,
) -> str:
    """Build the user prompt for hint generation."""
    problem = context.get("problem", {})
    concepts = context.get("concepts", [])
    prereqs = context.get("prerequisites", [])
    mastery = context.get("student_mastery", {})

    parts = []
    parts.append(f"Problem: {problem.get('title', 'Unknown')} ({problem.get('difficulty', 'N/A')})")

    if concepts:
        primary = [c["name"] for c in concepts if c.get("is_primary")]
        secondary = [c["name"] for c in concepts if not c.get("is_primary")]
        parts.append(f"Key concept(s): {', '.join(primary)}")
        if secondary:
            parts.append(f"Related concept(s): {', '.join(secondary)}")

    if prereqs:
        parts.append(f"Prerequisites: {', '.join(p['name'] for p in prereqs[:5])}")

    if mastery:
        weak_concepts = [
            name for name, m in mastery.items() if m["mastery"] < 0.5
        ]
        if weak_concepts:
            parts.append(f"Student struggles with: {', '.join(weak_concepts)}")

    parts.append(f"\nStudent's code:\n```python\n{student_code[:1500]}\n```")

    if error_message:
        parts.append(f"\nError: {error_message[:500]}")

    # Hint level controls progressiveness
    if hint_level == 1:
        parts.append("\nProvide a gentle, high-level hint. Ask a guiding question about the approach.")
    elif hint_level == 2:
        parts.append("\nProvide a more specific hint. Point to the exact concept or technique needed.")
    elif hint_level >= 3:
        parts.append(
            "\nProvide a detailed hint. Explain the algorithm or data structure step-by-step, "
            "but still don't give the complete code. Use pseudocode if needed."
        )

    return "\n".join(parts)


async def generate_hint(
    session: AsyncSession,
    student_id: str,
    problem_id: str,
    student_code: str,
    error_message: str | None = None,
    hint_level: int = 1,
) -> dict:
    """
    Generate a Socratic hint using LLM + knowledge graph context.

    Returns:
        {"hint": str, "concepts_referenced": list, "hint_level": int}
        or {"error": str} on failure
    """
    if not settings.enable_llm:
        return {"error": "LLM hints are disabled", "hint": None}

    if not settings.openai_api_key:
        return {"error": "OpenAI API key not configured", "hint": None}

    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Please try again in a minute.", "hint": None}

    try:
        # Lazy import to avoid startup dependency if LLM is disabled
        import openai

        client = openai.AsyncOpenAI(api_key=settings.openai_api_key)

        # Build context from knowledge graph
        context = await _build_context(session, student_id, problem_id)
        if not context.get("problem"):
            return {"error": "Problem not found", "hint": None}

        user_prompt = _build_hint_prompt(context, student_code, error_message, hint_level)

        response = await asyncio.wait_for(
            client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=settings.llm_max_tokens,
                temperature=0.7,
            ),
            timeout=15.0,  # 15 second timeout
        )

        hint_text = response.choices[0].message.content

        concepts_referenced = [c["name"] for c in context.get("concepts", [])]

        return {
            "hint": hint_text,
            "hint_level": hint_level,
            "concepts_referenced": concepts_referenced,
            "tokens_used": response.usage.total_tokens if response.usage else 0,
        }

    except ImportError:
        logger.warning("openai package not installed — LLM hints unavailable")
        return {"error": "openai package not installed", "hint": None}
    except asyncio.TimeoutError:
        logger.warning("LLM hint generation timed out")
        return {"error": "Hint generation timed out. Please try again.", "hint": None}
    except Exception as e:
        logger.error(f"LLM hint generation failed: {e}")
        return {"error": f"Hint generation failed: {str(e)}", "hint": None}
