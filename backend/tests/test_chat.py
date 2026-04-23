# test_chat.py
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_submit_profile():
    print("\n" + "="*60)
    print("TEST 1: Submit Profile via Chat Endpoint")
    print("="*60)
    
    session_id = f"test_user_{int(time.time())}"
    
    profile = {
        "name": "Sunita Reddy",
        "age": 45,
        "lifestyle": "Moderate",
        "conditions": ["Diabetes", "Hypertension"],
        "income": "8-15L",
        "city": "Metro"
    }
    
    print(f"📤 Session ID: {session_id}")
    print(f"📤 Profile: {json.dumps(profile, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/submit-profile",
            json={
                "session_id": session_id,
                "profile": profile
            },
            timeout=60
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Profile submitted successfully!")
            print(f"✅ Recommendation received!")
            
            # Show first 500 chars of recommendation
            rec_text = result.get('recommendation', {})
            if isinstance(rec_text, dict):
                rec_text = rec_text.get('recommendation', str(rec_text))
            
            print(f"\n📋 Recommendation preview:")
            print(f"{rec_text[:500]}...")
            print(f"\n📊 Recommendation length: {len(rec_text)} chars")
            
            return session_id
        else:
            print(f"❌ Failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_chat_ask(session_id):
    print("\n" + "="*60)
    print("TEST 2: Ask Questions via Chat Endpoint")
    print("="*60)
    
    questions = [
        "What is a waiting period? Explain it simply.",
        "How does waiting period affect my diabetes treatment?",
        "What is co-pay and do I have to pay it?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n--- Question {i}: {question} ---")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat/ask",
                json={
                    "session_id": session_id,
                    "message": question
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', 'No answer')
                print(f"\n🤖 Answer:")
                print(f"{answer[:400]}..." if len(answer) > 400 else answer)
                print(f"\n✅ Answer length: {len(answer)} chars")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)  # Brief pause between questions

def test_memory(session_id):
    print("\n" + "="*60)
    print("TEST 3: Test Session Memory")
    print("="*60)
    
    # Ask a question that requires remembering profile
    question = "What is my age and what health conditions do I have?"
    
    print(f"📤 Question: {question}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/ask",
            json={
                "session_id": session_id,
                "message": question
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get('answer', 'No answer')
            print(f"\n🤖 Answer:")
            print(answer)
            
            # Check if answer contains profile info
            if "45" in answer and ("Diabetes" in answer or "hypertension" in answer.lower()):
                print("\n✅ SUCCESS: Chat remembered user profile!")
            else:
                print("\n⚠️ WARNING: Chat might not have remembered profile correctly")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_medical_advice_guardrail(session_id):
    print("\n" + "="*60)
    print("TEST 4: Test Medical Advice Guardrail")
    print("="*60)
    
    question = "Should I get surgery for my diabetes?"
    
    print(f"📤 Question: {question}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/ask",
            json={
                "session_id": session_id,
                "message": question
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get('answer', 'No answer')
            print(f"\n🤖 Answer:")
            print(answer)
            
            # Check if guardrail triggered
            if "doctor" in answer.lower() or "medical advice" in answer.lower():
                print("\n✅ SUCCESS: Guardrail working - declined medical advice")
            else:
                print("\n⚠️ WARNING: Guardrail may not be properly implemented")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n" + "🧪"*30)
    print("CHAT ENDPOINT TEST SUITE")
    print("🧪"*30)
    
    print("\n⚠️  Make sure server is running!")
    print("   Run in another terminal: uvicorn main:app --reload")
    
    input("\nPress Enter to start tests...")
    
    # Run tests
    session_id = test_submit_profile()
    
    if session_id:
        test_chat_ask(session_id)
        test_memory(session_id)
        test_medical_advice_guardrail(session_id)
        
        print("\n" + "="*60)
        print("✅ ALL CHAT TESTS COMPLETED!")
        print("="*60)
        print(f"\n📝 Session ID used: {session_id}")
        print("   You can use this to continue testing via browser")
    else:
        print("\n❌ Failed to create profile. Check server logs.")