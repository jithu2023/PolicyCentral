# test_api.py
import requests
import json

BASE_URL = "http://localhost:8000"

# Test home
print("Testing home endpoint...")
r = requests.get(f"{BASE_URL}/")
print(f"Home: {r.json()}")

# Test recommendation
print("\nTesting recommendation...")
profile = {
    "name": "Rajesh Kumar",
    "age": 52,
    "lifestyle": "Sedentary",
    "conditions": ["Diabetes", "Hypertension"],
    "income": "8-15L",
    "city": "Tier-2"
}

r = requests.post(f"{BASE_URL}/recommendation/recommend", json=profile)
print(f"Recommendation status: {r.status_code}")
if r.status_code == 200:
    result = r.json()
    print(f"Recommendation received (length: {len(str(result))} chars)")
else:
    print(f"Error: {r.text}")

print("\n✅ API tests completed!")