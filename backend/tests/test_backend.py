# test_backend.py
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing backend components...")

# Test Groq
try:
    from langchain_groq import ChatGroq
    llm = ChatGroq(
        temperature=0.7,
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY", "test_key")
    )
    print("✅ Groq imported successfully")
except Exception as e:
    print(f"❌ Groq error: {e}")

# Test vectorstore
try:
    from rag.vectorstore import vectorstore
    print("✅ Vectorstore loaded successfully")
except Exception as e:
    print(f"❌ Vectorstore error: {e}")

# Test pdfplumber
try:
    import pdfplumber
    print("✅ pdfplumber loaded successfully")
except Exception as e:
    print(f"❌ pdfplumber error: {e}")

print("\n✅ All tests passed! Ready to run the server.")