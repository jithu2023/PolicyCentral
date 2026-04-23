# backend/routes/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_profile, save_profile
from rag.vectorstore import vectorstore
from core.llm import get_llm

router = APIRouter(prefix="/chat")

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ProfileSubmitRequest(BaseModel):
    session_id: str
    profile: dict

@router.post("/submit-profile")
async def submit_profile(request: ProfileSubmitRequest):
    """Save user profile and generate recommendation"""
    from services.recommendation_service import generate_recommendation
    
    # Save profile
    save_profile(request.session_id, request.profile)
    
    # Generate recommendation
    recommendation = generate_recommendation(request.profile)
    
    return {
        "status": "success",
        "recommendation": recommendation
    }

@router.post("/ask")
async def ask_question(request: ChatRequest):
    """Chat with the AI about the recommended policy"""
    
    # Get user profile
    profile = get_profile(request.session_id)
    if not profile:
        raise HTTPException(status_code=400, detail="No profile found. Please submit profile first.")
    
    llm = get_llm()
    
    # Search relevant policy chunks
    query = f"User question about insurance: {request.message}"
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    
    conditions_str = ", ".join(profile.get('conditions', []))
    
    prompt = f"""You are a health insurance explainer helping {profile['name']} (age {profile['age']}, {profile['lifestyle']} lifestyle, from {profile['city']} city).

Health conditions: {conditions_str if conditions_str else 'None'}

Policy information from documents:
{context}

User's question: {request.message}

IMPORTANT RULES:
1. Define any insurance term the first time you use it
2. Give a realistic example using their actual condition ({conditions_str}) if relevant
3. Always cite the policy document as your source
4. If asked for medical advice, say: "I can only help with insurance questions. Please consult a doctor."
5. Remember their profile - don't ask for age/conditions again
6. Be empathetic and warm

Answer helpfully:"""
    
    response = llm.invoke(prompt)
    answer = response.content if hasattr(response, 'content') else str(response)
    
    return {"answer": answer}