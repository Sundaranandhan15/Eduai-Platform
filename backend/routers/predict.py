from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np

from auth import get_current_user
from models import User
from triton_client import TritonDKTClient

router = APIRouter(prefix="/api/predict", tags=["predict"])

class PredictRequest(BaseModel):
    skill_seq: List[int]
    correct_seq: List[int]

class PredictResponse(BaseModel):
    mastery_probabilities: List[float]

@router.post("/", response_model=PredictResponse)
def predict_mastery(request: PredictRequest, current_user: User = Depends(get_current_user)):
    if len(request.skill_seq) != len(request.correct_seq):
        raise HTTPException(status_code=400, detail="skill_seq and correct_seq must have the same length")
    
    try:
        client = TritonDKTClient()
        preds = client.predict(request.skill_seq, request.correct_seq)
        
        # We only return the latest step predictions. 
        # preds shape: (num_skills,)
        return {"mastery_probabilities": preds.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
