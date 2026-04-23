# backend/services/recommendation_service.py
from rag.vectorstore import vectorstore
from core.llm import get_llm

def generate_recommendation(user_profile):
    llm = get_llm()
    
    # Build query from profile
    conditions_str = ", ".join(user_profile.get('conditions', []))
    
    query = f"""
    Health insurance needed for:
    - {user_profile['age']} year old
    - {user_profile['lifestyle']} lifestyle  
    - Health conditions: {conditions_str if conditions_str else 'None'}
    - Income: {user_profile['income']}
    - City type: {user_profile['city']}
    """
    
    # Get relevant policies from vector store
    docs = vectorstore.similarity_search(query, k=5)
    context = "\n\n---\n\n".join([d.page_content for d in docs])
    
    prompt = f"""You are a health insurance advisor. Based ONLY on the policy documents below, recommend a policy.

USER PROFILE:
Name: {user_profile.get('name', 'Customer')}
Age: {user_profile['age']}
Lifestyle: {user_profile['lifestyle']}  
Health Conditions: {conditions_str if conditions_str else 'None'}
Annual Income: {user_profile['income']}
City Tier: {user_profile['city']}

AVAILABLE POLICIES (from documents):
{context}

IMPORTANT: Generate 3 DIFFERENT policies in comparison table. DO NOT repeat the same policy.

Generate response in EXACTLY this format:

BEST POLICY: [Policy Name] by [Insurer]

COMPARISON TABLE:
| Policy Name | Insurer | Premium (Rs/yr) | Cover Amount | Waiting Period (months) | Key Benefit | Suitability Score |
|-------------|---------|----------------|--------------|------------------------|-------------|-------------------|
| [Unique Policy 1] | [Insurer] | [Amount] | [Amount] | [Months] | [One key benefit] | [Score]/10 |
| [Unique Policy 2] | [Insurer] | [Amount] | [Amount] | [Months] | [One key benefit] | [Score]/10 |
| [Unique Policy 3] | [Insurer] | [Amount] | [Amount] | [Months] | [One key benefit] | [Score]/10 |

COVERAGE DETAILS FOR BEST POLICY:
- Inclusions: [List 3-5 inclusions]
- Exclusions: [List 3-5 exclusions]
- Sub-limits: [Any limits]
- Co-pay: [Percentage or None]
- Claim Type: [Cashless/Reimbursement/Both]

WHY THIS POLICY FOR {user_profile.get('name', 'YOU').upper()}:
[Write 150-250 words that:
1. Acknowledge their health conditions with empathy
2. Explain why this policy fits their age ({user_profile['age']})
3. Address their {conditions_str if conditions_str else 'good health'} specifically
4. Connect to their income level ({user_profile['income']})
5. Mention city tier ({user_profile['city']}) and network hospital access]

RULES:
- Use ONLY information from documents above
- NEVER repeat the same policy twice in comparison
- If policy lacks info, write "Not specified"
- Be warm and empathetic
- Define any insurance terms

Now generate recommendation:"""
    
    response = llm.invoke(prompt)
    result = response.content if hasattr(response, 'content') else str(response)
    
    return {
        "recommendation": result,
        "profile_used": user_profile
    }