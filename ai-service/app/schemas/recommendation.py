from pydantic import BaseModel


class RecommendedProblem(BaseModel):
    problem_id: str
    title: str
    difficulty: str
    score: float


class RecommendationsResponse(BaseModel):
    user_id: str
    recommendations: list[RecommendedProblem]
