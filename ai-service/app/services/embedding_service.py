import uuid

import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import ProblemEmbedding


class EmbeddingService:
    def __init__(self, model: SentenceTransformer):
        self.model = model

    def encode(self, content: str) -> list[float]:
        vec = self.model.encode(content, normalize_embeddings=True)
        return vec.tolist()

    def encode_batch(self, contents: list[str]) -> list[list[float]]:
        vecs = self.model.encode(contents, normalize_embeddings=True, batch_size=32)
        return vecs.tolist()

    async def embed_problem(
        self,
        session: AsyncSession,
        problem_id: str,
        title: str,
        description: str,
        concepts: list[str] | None = None,
    ) -> list[float]:
        concept_text = ' '.join(concepts) if concepts else ''
        content = f"{title}\n{description}\n{concept_text}"
        embedding = self.encode(content)

        # Upsert into problem_embeddings (both Float[] and vector columns)
        embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
        await session.execute(
            text("""
                INSERT INTO problem_embeddings (id, "problemId", embedding, embedding_vec, "updatedAt")
                VALUES (:id, :problem_id, :embedding, :embedding_vec, NOW())
                ON CONFLICT ("problemId")
                DO UPDATE SET embedding = :embedding, embedding_vec = :embedding_vec, "updatedAt" = NOW()
            """),
            {
                "id": str(uuid.uuid4()),
                "problem_id": problem_id,
                "embedding": embedding,
                "embedding_vec": embedding_str,
            },
        )
        await session.commit()
        return embedding

    async def embed_batch(
        self,
        session: AsyncSession,
        problems: list[dict],
    ) -> list[dict]:
        contents = [
            f"{p['title']}\n{p['description']}\n{' '.join(p.get('concepts', p.get('tags', [])))}"
            for p in problems
        ]
        embeddings = self.encode_batch(contents)

        results = []
        for problem, embedding in zip(problems, embeddings):
            embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
            await session.execute(
                text("""
                    INSERT INTO problem_embeddings (id, "problemId", embedding, embedding_vec, "updatedAt")
                    VALUES (:id, :problem_id, :embedding, :embedding_vec, NOW())
                    ON CONFLICT ("problemId")
                    DO UPDATE SET embedding = :embedding, embedding_vec = :embedding_vec, "updatedAt" = NOW()
                """),
                {
                    "id": str(uuid.uuid4()),
                    "problem_id": problem["problem_id"],
                    "embedding": embedding,
                    "embedding_vec": embedding_str,
                },
            )
            results.append({"problem_id": problem["problem_id"], "embedding": embedding})

        await session.commit()
        return results
