# test_delete.py
import requests
import time

BASE_URL = "http://localhost:8000"

def test_delete_policy():
    print("="*50)
    print("Testing Delete Policy Functionality")
    print("="*50)
    
    # First, list current policies
    print("\n1. Listing current policies...")
    response = requests.get(
        f"{BASE_URL}/admin/policies",
        auth=("admin", "admin123")
    )
    
    if response.status_code == 200:
        policies = response.json().get('policies', [])
        print(f"   Found {len(policies)} policies:")
        for p in policies:
            print(f"   - {p.get('name')} ({p.get('source')})")
        
        if policies:
            # Delete the first policy
            policy_to_delete = policies[0]['source']
            print(f"\n2. Deleting policy: {policy_to_delete}")
            
            delete_response = requests.delete(
                f"{BASE_URL}/admin/policy/{policy_to_delete}",
                auth=("admin", "admin123")
            )
            
            print(f"   Status: {delete_response.status_code}")
            print(f"   Response: {delete_response.json()}")
            
            # Wait a moment for deletion to process
            time.sleep(1)
            
            # List policies again to verify deletion
            print("\n3. Listing policies after deletion...")
            response2 = requests.get(
                f"{BASE_URL}/admin/policies",
                auth=("admin", "admin123")
            )
            
            if response2.status_code == 200:
                new_policies = response2.json().get('policies', [])
                print(f"   Found {len(new_policies)} policies remaining")
                
                # Check if deleted policy is gone
                deleted_found = any(p.get('source') == policy_to_delete for p in new_policies)
                if not deleted_found:
                    print(f"\n✅ SUCCESS: Policy '{policy_to_delete}' was deleted successfully!")
                else:
                    print(f"\n❌ FAIL: Policy '{policy_to_delete}' still exists!")
        else:
            print("\n   No policies to delete. Upload some policies first.")
    else:
        print(f"❌ Failed to list policies: {response.status_code}")

if __name__ == "__main__":
    test_delete_policy()