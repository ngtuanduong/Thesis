from contextlib import asynccontextmanager

from fastapi import FastAPI
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.routers import embed, profile, recommend, skill_gap
from app.services.embedding_service import EmbeddingService
from app.services.profile_service import ProfileService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model once at startup
    model = SentenceTransformer(settings.embedding_model)
    app.state.embedding_service = EmbeddingService(model)
    app.state.profile_service = ProfileService(model)
    yield


app = FastAPI(title="Adaptive Learning AI Service", lifespan=lifespan)

app.include_router(embed.router)
app.include_router(profile.router)
app.include_router(recommend.router)
app.include_router(skill_gap.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
