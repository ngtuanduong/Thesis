"""
Chatbot Q&A endpoints.

Provides AI-powered responses about platform usage and programming learning.
"""

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends

from app.dependencies import verify_service_key
from app.services.chatbot_service import generate_response

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
    dependencies=[Depends(verify_service_key)],
)


class ConversationMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str


class ChatbotRequest(BaseModel):
    message: str = Field(..., max_length=1000)
    conversation_history: list[ConversationMessage] = Field(default_factory=list)
    user_role: str = Field(..., pattern="^(STUDENT|INSTRUCTOR|ADMIN)$")


class ChatbotResponse(BaseModel):
    response: str | None = None
    tokens_used: int = 0
    error: str | None = None


@router.post("/respond", response_model=ChatbotResponse)
async def chatbot_respond(request: ChatbotRequest):
    """Generate a chatbot response for a user message."""
    result = await generate_response(
        message=request.message,
        conversation_history=[msg.model_dump() for msg in request.conversation_history],
        user_role=request.user_role,
    )
    return ChatbotResponse(**result)
