# backend/core/llm.py
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Get the absolute path to backend directory
backend_dir = Path(__file__).parent.parent
env_file = backend_dir / '.env'

# Load .env from exact location
load_dotenv(dotenv_path=env_file)

_llm = None

def get_llm():
    global _llm
    
    if _llm is None:
        print(" Loading Groq LLM once...")
        
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            print(f" .env file path: {env_file}")
            print(f" .env exists: {env_file.exists()}")
            if env_file.exists():
                print("❌ Content of .env (first 100 chars):")
                with open(env_file) as f:
                    print(f.read()[:100])
            raise ValueError("GROQ_API_KEY not found")
        
        print(f"✅ API Key loaded (first 10 chars): {api_key[:10]}...")
        
        _llm = ChatGroq(
            temperature=0.7,
            model="llama-3.3-70b-versatile",
            api_key=api_key
        )
        
        print("✅ Groq LLM loaded successfully")
    
    return _llm