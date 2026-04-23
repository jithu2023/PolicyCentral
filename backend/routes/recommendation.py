from fastapi import APIRouter
from services.recommendation_service import generate_recommendation

router = APIRouter(prefix="/recommendation")

@router.post("/recommend")
def recommend(user_profile: dict):
    result = generate_recommendation(user_profile)
    return {"result": result}