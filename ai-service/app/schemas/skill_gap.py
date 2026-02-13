from pydantic import BaseModel


class SkillGapItem(BaseModel):
    skill_name: str
    current_score: float
    target_score: float
    gap: float


class SkillGapResponse(BaseModel):
    user_id: str
    gaps: list[SkillGapItem]
