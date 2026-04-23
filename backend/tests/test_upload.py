# test_upload.py
import requests
import os

BASE_URL = "http://localhost:8000"

def upload_policy(file_path):
    filename = os.path.basename(file_path)
    print(f"\n📤 Uploading {filename}...")
    
    # Determine mime type
    if filename.endswith('.pdf'):
        mime_type = "application/pdf"
    elif filename.endswith('.json'):
        mime_type = "application/json"
    else:
        mime_type = "text/plain"
    
    with open(file_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/admin/upload-policy",
            files={"file": (filename, f, mime_type)},
            auth=("admin", "admin123")
        )
    
    print(f"   Status: {response.status_code}")
    result = response.json()
    if result.get('success'):
        print(f"   ✅ {result.get('message')}")
        print(f"   📊 {result.get('chunks')} chunks created")
    else:
        print(f"   ❌ Error: {result.get('error')}")
    
    return response

if __name__ == "__main__":
    print("="*50)
    print("Uploading Sample Policies (TXT, JSON, PDF)")
    print("="*50)
    
    policy_files = [
        "sample_policies/policy1.txt",
        "sample_policies/policy2.json",
        "sample_policies/policy3.pdf"
    ]
    
    for policy_file in policy_files:
        if os.path.exists(policy_file):
            upload_policy(policy_file)
        else:
            print(f"\n❌ Not found: {policy_file}")
            print("   Run 'python create_sample_policies.py' first")
    
    print("\n" + "="*50)
    print("✅ Upload complete!")
    print("="*50)