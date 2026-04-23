# backend/rag/vectorstore.py - Robust version
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import shutil

# Initialize embeddings
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

persist_dir = "./chroma_db"

# Ensure directory exists
os.makedirs(persist_dir, exist_ok=True)

# Create vectorstore with error handling
try:
    vectorstore = Chroma(
        collection_name="policies",
        embedding_function=embedding,
        persist_directory=persist_dir
    )
    print("✅ Vectorstore connected successfully")
except Exception as e:
    print(f"⚠️ Error connecting to vectorstore: {e}")
    print("Creating new vectorstore...")
    
    # If connection fails, try to recreate
    try:
        # Remove existing directory if corrupt
        if os.path.exists(persist_dir):
            shutil.rmtree(persist_dir)
            os.makedirs(persist_dir, exist_ok=True)
        
        vectorstore = Chroma(
            collection_name="policies",
            embedding_function=embedding,
            persist_directory=persist_dir
        )
        print("✅ New vectorstore created")
    except Exception as e2:
        print(f"❌ Failed to create vectorstore: {e2}")
        raise