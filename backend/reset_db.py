# reset_db.py - Updated (remove .persist)
from rag.vectorstore import vectorstore
import os
import shutil

print("🗑️ Clearing vector database...")

try:
    # Try to delete collection
    vectorstore.delete_collection()
    print("✅ Collection deleted")
except Exception as e:
    print(f"Could not delete collection: {e}")

# Also delete the directory for fresh start
if os.path.exists("./chroma_db"):
    shutil.rmtree("./chroma_db")
    print("✅ chroma_db folder deleted")

print("✅ Database cleared successfully! Next upload will create fresh collection.")