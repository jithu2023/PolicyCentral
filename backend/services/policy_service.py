# backend/services/policy_service.py
import pdfplumber
import json
import os
from rag.vectorstore import vectorstore

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    text = ""
    try:
        file.file.seek(0)
        
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        
        if not text.strip():
            text = "No text content found in PDF"
            
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        text = f"Error processing PDF: {str(e)}"
    
    return text

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    try:
        file.file.seek(0)
        content = file.file.read()
        
        if isinstance(content, bytes):
            text = content.decode('utf-8')
        else:
            text = str(content)
        
        return text
    except Exception as e:
        print(f"Error extracting TXT text: {e}")
        return f"Error processing TXT: {str(e)}"

def extract_text_from_json(file):
    """Extract text from JSON file"""
    try:
        file.file.seek(0)
        content = file.file.read()
        
        if isinstance(content, bytes):
            data = json.loads(content.decode('utf-8'))
        else:
            data = json.loads(content)
        
        # Convert JSON to readable text
        text = ""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    text += f"{key}:\n"
                    for sub_key, sub_value in value.items():
                        text += f"  {sub_key}: {sub_value}\n"
                    text += "\n"
                elif isinstance(value, list):
                    text += f"{key}: {', '.join(str(v) for v in value)}\n"
                else:
                    text += f"{key}: {value}\n"
        else:
            text = json.dumps(data, indent=2)
        
        return text if text.strip() else "No readable content in JSON"
        
    except Exception as e:
        print(f"Error extracting JSON text: {e}")
        return f"Error processing JSON: {str(e)}"

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into chunks with overlap"""
    if not text or text.startswith("Error"):
        return []
    
    words = text.split()
    chunks = []
    step = chunk_size - overlap
    
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

async def process_policy(file):
    """Process uploaded policy document - supports PDF, TXT, JSON"""
    try:
        filename = file.filename
        file_extension = filename.lower().split('.')[-1]
        
        print(f"📄 Processing file: {filename} (Type: {file_extension})")
        
        # Extract text based on file type
        if file_extension == 'pdf':
            text = extract_text_from_pdf(file)
            file_type = "PDF"
        elif file_extension == 'txt':
            text = extract_text_from_txt(file)
            file_type = "Text"
        elif file_extension == 'json':
            text = extract_text_from_json(file)
            file_type = "JSON"
        else:
            return {"error": f"Unsupported file type: {file_extension}. Please upload PDF, TXT, or JSON"}
        
        # Check if extraction was successful
        if not text or text.startswith("Error"):
            return {"error": text or f"Failed to extract text from {file_type} file"}
        
        print(f"✅ Extracted {len(text)} characters from {file_type} file")
        
        # Split into chunks
        chunks = chunk_text(text)
        
        if not chunks:
            return {"error": "No content chunks created"}
        
        print(f"📦 Created {len(chunks)} chunks")
        
        # Extract policy name from filename
        policy_name = filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
        
        # Add metadata for each chunk
        metadatas = [{
            "source": filename,
            "type": "policy",
            "file_type": file_type,
            "chunk_id": i,
            "policy_name": policy_name,
            "total_chunks": len(chunks)
        } for i in range(len(chunks))]
        
        # Add to vectorstore (auto-persists in new ChromaDB)
        vectorstore.add_texts(chunks, metadatas=metadatas)
        # REMOVED: vectorstore.persist() - no longer needed!
        
        print(f"💾 Stored {len(chunks)} chunks in vector database")
        
        return {
            "success": True,
            "message": f"Policy '{policy_name}' processed & stored successfully ✅",
            "chunks": len(chunks),
            "filename": filename,
            "policy_name": policy_name,
            "file_type": file_type,
            "characters": len(text)
        }
        
    except Exception as e:
        print(f"❌ Processing error: {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"Processing failed: {str(e)}"}