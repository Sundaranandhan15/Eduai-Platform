from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import get_db
from models import User, Interaction
from auth import get_current_user

router = APIRouter(prefix="/api/submit", tags=["submit"])

class SubmitRequest(BaseModel):
    skill_id: int
    problem_id: int
    correct: int

class SubmitResponse(BaseModel):
    success: bool
    interaction_id: int

@router.post("/", response_model=SubmitResponse)
def submit_interaction(request: SubmitRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    interaction = Interaction(
        user_id=current_user.id,
        skill_id=request.skill_id,
        problem_id=request.problem_id,
        correct=request.correct
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    
    return {"success": True, "interaction_id": interaction.id}
