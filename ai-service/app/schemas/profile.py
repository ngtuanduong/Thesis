from pydantic import BaseModel


class SkillScore(BaseModel):
    skill_name: str
    score: float


class ProfileResponse(BaseModel):
    user_id: str
    skills: list[SkillScore]
