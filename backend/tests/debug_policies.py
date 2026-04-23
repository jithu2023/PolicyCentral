# debug_policies.py
from rag.vectorstore import vectorstore

print("🔍 Debugging Vector Store Contents")
print("="*50)

try:
    # Try to get all documents
    results = vectorstore.similarity_search("health insurance", k=30)
    
    print(f"\nTotal chunks found: {len(results)}")
    
    if len(results) == 0:
        print("\n⚠️ No documents found in vector store!")
        print("You need to upload policies first.")
        print("\nRun this to upload sample policies:")
        print("python test_upload.py")
    else:
        print("\n📚 Documents found:")
        unique_sources = {}
        
        for i, doc in enumerate(results[:10]):  # Show first 10
            source = doc.metadata.get('source', 'No source')
            if source not in unique_sources:
                unique_sources[source] = 0
            unique_sources[source] += 1
            
            print(f"\n{i+1}. Source: {source}")
            print(f"   Preview: {doc.page_content[:100]}...")
        
        print(f"\n\n📊 Summary:")
        print(f"Total unique policy sources: {len(unique_sources)}")
        for source, count in unique_sources.items():
            print(f"  - {source}: {count} chunks")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()