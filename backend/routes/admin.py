# backend/routes/admin.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import os
import urllib.parse
from services.policy_service import process_policy
from rag.vectorstore import vectorstore

router = APIRouter(prefix="/admin")
security = HTTPBasic()

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "admin123")

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USER or credentials.password != ADMIN_PASS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return True

# Pydantic model for policy update request
class PolicyUpdate(BaseModel):
    policy_name: str
    insurer: str

@router.post("/upload-policy")
async def upload_policy(
    file: UploadFile = File(...),
    auth: bool = Depends(verify_admin)
):
    return await process_policy(file)

@router.get("/policies")
async def list_policies(auth: bool = Depends(verify_admin)):
    """List all policies in the vector store"""
    try:
        # Get all documents from vectorstore
        results = vectorstore.similarity_search("", k=100)
        
        # Extract unique policy sources
        policies_dict = {}
        for doc in results:
            source = doc.metadata.get('source', 'Unknown')
            policy_name = doc.metadata.get('policy_name', source.replace('.txt', '').replace('.pdf', '').replace('.json', ''))
            insurer = doc.metadata.get('insurer', 'Not specified')
            
            if source not in policies_dict:
                policies_dict[source] = {
                    "id": source,
                    "name": policy_name,
                    "insurer": insurer,
                    "source": source,
                    "file_type": doc.metadata.get('file_type', 'Unknown'),
                    "date": "Recently uploaded",
                    "chunks": 1
                }
            else:
                policies_dict[source]["chunks"] += 1
        
        policies = list(policies_dict.values())
        return {"policies": policies}
        
    except Exception as e:
        print(f"Error listing policies: {e}")
        return {"policies": []}

@router.put("/policy/{policy_id}")
async def update_policy(
    policy_id: str,
    update: PolicyUpdate,
    auth: bool = Depends(verify_admin)
):
    """Edit policy name and insurer metadata after upload"""
    try:
        decoded_policy_id = urllib.parse.unquote(policy_id)
        
        print(f"✏️ Editing policy: {decoded_policy_id}")
        print(f"   New name: {update.policy_name}")
        print(f"   New insurer: {update.insurer}")
        
        # Get the collection directly
        collection = vectorstore._collection
        
        # Get all documents with matching source
        all_docs = collection.get(
            where={"source": decoded_policy_id}, 
            include=["metadatas", "documents"]
        )
        
        if not all_docs or not all_docs['ids']:
            raise HTTPException(
                status_code=404, 
                detail=f"Policy '{decoded_policy_id}' not found in vector store"
            )
        
        # Update metadata for all chunks
        updated_metadatas = []
        for metadata in all_docs['metadatas']:
            if metadata:
                metadata['policy_name'] = update.policy_name
                metadata['insurer'] = update.insurer
                updated_metadatas.append(metadata)
            else:
                # Create new metadata if none existed
                updated_metadatas.append({
                    "source": decoded_policy_id,
                    "policy_name": update.policy_name,
                    "insurer": update.insurer,
                    "type": "policy"
                })
        
        # Delete old documents
        collection.delete(where={"source": decoded_policy_id})
        
        # Re-add with updated metadata
        collection.add(
            ids=all_docs['ids'],
            documents=all_docs['documents'],
            metadatas=updated_metadatas
        )
        
        print(f"✅ Updated {len(all_docs['ids'])} chunks for {decoded_policy_id}")
        
        return {
            "success": True,
            "message": f"Policy updated: '{update.policy_name}' (Insurer: {update.insurer})",
            "chunks_updated": len(all_docs['ids'])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Edit error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Edit failed: {str(e)}")

@router.delete("/policy/{policy_id}")
async def delete_policy(
    policy_id: str,
    auth: bool = Depends(verify_admin)
):
    """Delete a policy by its source filename from vector store"""
    try:
        decoded_policy_id = urllib.parse.unquote(policy_id)
        
        print(f"🗑️ Attempting to delete: {decoded_policy_id}")
        
        # Get the collection directly
        collection = vectorstore._collection
        
        # Get all documents with their IDs and metadata
        all_docs = collection.get(where={"source": decoded_policy_id}, include=["metadatas"])
        
        if all_docs and all_docs['ids']:
            deleted_count = len(all_docs['ids'])
            
            # Delete the documents
            collection.delete(ids=all_docs['ids'])
            
            print(f"✅ Deleted {deleted_count} chunks for {decoded_policy_id}")
            
            return {
                "success": True,
                "message": f"Policy '{decoded_policy_id}' deleted successfully",
                "chunks_deleted": deleted_count
            }
        else:
            return {
                "success": False,
                "message": f"Policy '{decoded_policy_id}' not found in vector store"
            }
        
    except Exception as e:
        print(f"❌ Delete error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")