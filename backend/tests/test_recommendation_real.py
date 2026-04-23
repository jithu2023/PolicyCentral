# test_recommendation_real.py
import requests
import json

BASE_URL = "http://localhost:8000"

# Test different user profiles
test_profiles = [
    {
        "name": "Rajesh Kumar",
        "age": 52,
        "lifestyle": "Sedentary",
        "conditions": ["Diabetes", "Hypertension"],
        "income": "8-15L",
        "city": "Tier-2"
    },
    {
        "name": "Priya Sharma",
        "age": 35,
        "lifestyle": "Moderate",
        "conditions": ["Asthma"],
        "income": "15L+",
        "city": "Metro"
    },
    {
        "name": "Amit Patel",
        "age": 28,
        "lifestyle": "Active",
        "conditions": [],
        "income": "3-8L",
        "city": "Tier-3"
    }
]

for i, profile in enumerate(test_profiles, 1):
    print(f"\n{'='*70}")
    print(f"Test {i}: {profile['name']} - Age {profile['age']}, {profile['city']}")
    print(f"{'='*70}")
    
    response = requests.post(
        f"{BASE_URL}/recommendation/recommend",
        json=profile
    )
    
    if response.status_code == 200:
        result = response.json()
        print(result['result'])
    else:
        print(f"Error: {response.text}")
    
    input("\nPress Enter for next test...")