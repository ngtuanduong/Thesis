from pydantic import BaseModel


class EmbedProblemRequest(BaseModel):
    problem_id: str
    title: str
    description: str
    tags: list[str] = []


class EmbedBatchRequest(BaseModel):
    problems: list[EmbedProblemRequest]


class EmbeddingResponse(BaseModel):
    problem_id: str
    embedding: list[float]


class EmbedBatchResponse(BaseModel):
    results: list[EmbeddingResponse]
