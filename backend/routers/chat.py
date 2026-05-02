from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth import get_current_user
from models import User
from agent import generate_tutor_response

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    question: str
    mastery_prob: float

class ChatResponse(BaseModel):
    hint: str

@router.post("/", response_model=ChatResponse)
def chat_with_tutor(request: ChatRequest, current_user: User = Depends(get_current_user)):
    try:
        hint = generate_tutor_response(request.question, request.mastery_prob)
        return {"hint": hint}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
