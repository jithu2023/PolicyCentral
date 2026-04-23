# backend/core/llm.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

_llm = None

def get_llm():
    global _llm
    
    if _llm is None:
        print("🔄 Loading Groq LLM once...")
        
        _llm = ChatGroq(
            temperature=0.7,
            model="llama-3.3-70b-versatile",  # Good free model
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        print("✅ Groq LLM loaded successfully")
    
    return _llm