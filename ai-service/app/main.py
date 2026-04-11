from contextlib import asynccontextmanager

from fastapi import FastAPI
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.routers import embed, profile, recommend, skill_gap, knowledge_tracing, elo, mab, fsrs, adaptive, hints, evaluation
from app.services.embedding_service import EmbeddingService
from app.services.profile_service import ProfileService
from app.services.cache_service import cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model once at startup
    model = SentenceTransformer(settings.embedding_model)
    app.state.embedding_service = EmbeddingService(model)
    app.state.profile_service = ProfileService(model)
    # Connect Redis cache
    await cache.connect()
    yield
    await cache.close()


app = FastAPI(title="Adaptive Learning AI Service", lifespan=lifespan)

app.include_router(embed.router)
app.include_router(profile.router)
app.include_router(recommend.router)
app.include_router(skill_gap.router)
app.include_router(knowledge_tracing.router)
app.include_router(elo.router)
app.include_router(mab.router)
app.include_router(fsrs.router)
app.include_router(adaptive.router)
app.include_router(hints.router)
app.include_router(evaluation.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
