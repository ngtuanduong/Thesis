from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_service_key
from app.schemas.embedding import (
    EmbedBatchRequest,
    EmbedBatchResponse,
    EmbeddingResponse,
    EmbedProblemRequest,
)

router = APIRouter(prefix="/embed", tags=["embedding"], dependencies=[Depends(verify_service_key)])


@router.post("/problem", response_model=EmbeddingResponse)
async def embed_problem(
    body: EmbedProblemRequest,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    embedding_service = request.app.state.embedding_service
    embedding = await embedding_service.embed_problem(
        session,
        problem_id=body.problem_id,
        title=body.title,
        description=body.description,
        concepts=body.tags,
    )
    return EmbeddingResponse(problem_id=body.problem_id, embedding=embedding)


@router.post("/batch", response_model=EmbedBatchResponse)
async def embed_batch(
    body: EmbedBatchRequest,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    embedding_service = request.app.state.embedding_service
    problems = [p.model_dump() for p in body.problems]
    results = await embedding_service.embed_batch(session, problems)
    return EmbedBatchResponse(
        results=[EmbeddingResponse(**r) for r in results]
    )
