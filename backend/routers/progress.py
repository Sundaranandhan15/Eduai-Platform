from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any

from database import get_db
from models import User, Interaction
from auth import get_current_user
from triton_client import TritonDKTClient

router = APIRouter(prefix="/api/progress", tags=["progress"])

class ProgressResponse(BaseModel):
    history: List[List[float]]

@router.get("/{user_id}", response_model=ProgressResponse)
def get_progress(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if user is requesting their own progress or if we need role checks (omitted for simplicity)
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this user's progress")
    
    interactions = db.query(Interaction).filter(Interaction.user_id == user_id).order_by(Interaction.timestamp).all()
    
    if not interactions:
        return {"history": []}

    skill_seq = [inter.skill_id for inter in interactions]
    correct_seq = [inter.correct for inter in interactions]
    
    try:
        # Re-initialize Triton client
        client = TritonDKTClient()
        
        # We need the full history. The predict method in our TritonClient currently returns the latest step.
        # Let's adjust or write custom logic here to get the full array.
        # But wait, triton_client.py: output_data[0] is shape (200, 198).
        # We padded at the beginning. So the actual sequence is at the end.
        
        preds = client.predict(skill_seq, correct_seq) # Returns shape (198,) in our current client...
        # Wait, our predict() in triton_client.py returns output_data[0][-1] ?
        # Actually it returns output_data[0] which is (200, 198).
        # Let's slice the relevant part!
        
        seq_len = len(skill_seq)
        max_seq_len = 200
        
        if seq_len > max_seq_len:
            actual_len = max_seq_len
        else:
            actual_len = seq_len
            
        # The padding was at the beginning: (pad_len, 0).
        # So the valid data is at the end: [-actual_len:]
        history = preds[-actual_len:].tolist()
        
        return {"history": history}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
