# create_sample_policies.py
import json

# Create sample_policies directory
import os
os.makedirs("sample_policies", exist_ok=True)

# 1. Create TXT policy
txt_content = """Policy Name: Aarogya Plus Health Insurance
Insurer: Star Health Insurance
Premium: Rs 12,000 per year
Cover Amount: Rs 5,00,000
Waiting Period for Pre-existing Diseases: 24 months
Waiting Period for Specific Diseases: 12 months
Co-pay: 10% for network hospitals, 20% for non-network
Claim Type: Cashless and Reimbursement

INCLUSIONS:
- Hospitalization expenses up to sum insured
- Daycare procedures (over 500 procedures)
- Pre-hospitalization expenses (60 days before admission)
- Post-hospitalization expenses (90 days after discharge)
- Ambulance charges up to Rs 2,500
- Organ donor expenses up to Rs 50,000

EXCLUSIONS:
- Dental treatments (unless accidental)
- Cosmetic surgery
- Alternative treatments (Ayurveda, Homeopathy)
- War and nuclear risks
- Self-inflicted injuries
- Substance abuse treatment

NETWORK HOSPITALS:
- Metro cities: 500+ hospitals
- Tier-2 cities: 200+ hospitals
- Tier-3 cities: 50+ hospitals
"""

with open("sample_policies/policy1.txt", "w", encoding="utf-8") as f:
    f.write(txt_content)
print("✅ Created sample_policies/policy1.txt")

# 2. Create JSON policy
json_content = {
    "policy_name": "Family First Complete Plan",
    "insurer": "HDFC ERGO",
    "premium": {
        "annual": 15000,
        "monthly": 1250,
        "for_age_30": 12000,
        "for_age_50": 18000
    },
    "cover_amount": 1000000,
    "waiting_periods": {
        "pre_existing_diseases": 36,
        "specific_diseases": 24,
        "maternity": 24
    },
    "co_pay": {
        "metro_hospitals": 0,
        "tier2_hospitals": 10,
        "tier3_hospitals": 20
    },
    "claim_type": "Cashless",
    "inclusions": [
        "Hospitalization expenses",
        "Maternity cover (after 24 months)",
        "Newborn baby cover from day 1",
        "Vaccination expenses up to Rs 3,000",
        "Health checkup every year",
        "No claim bonus: 10% increase each year"
    ],
    "exclusions": [
        "Pre-existing diseases first 36 months",
        "Obesity treatment",
        "Fertility treatments",
        "Experimental treatments",
        "Cosmetic surgery"
    ],
    "benefits": {
        "restoration_benefit": "100% sum insured restoration once per year",
        "cumulative_bonus": "Up to 50% increase for claim-free years",
        "daycare_procedures": "500+ procedures covered"
    }
}

with open("sample_policies/policy2.json", "w", encoding="utf-8") as f:
    json.dump(json_content, f, indent=2)
print("✅ Created sample_policies/policy2.json")

# 3. Create PDF policy (using reportlab)
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import sys
    
    pdf_content = """Care Basic Health Insurance Plan
    
Insurer: Care Health Insurance
Premium Range: Rs 5,000 - Rs 8,000 per year
Cover Amount: Rs 2,00,000 - Rs 5,00,000
Waiting Period for Pre-existing Diseases: 48 months
Co-pay: 30% for all claims
Claim Type: Reimbursement Only

Key Features:
- Affordable premium for basic coverage
- Cashless treatment at 3000+ network hospitals
- No claim bonus up to 20%
- Free annual health checkup after 2 years

Inclusions:
- Inpatient hospitalization
- Daycare procedures
- Pre-hospitalization (30 days)
- Post-hospitalization (60 days)
- Ambulance cover: Rs 1,500

Exclusions:
- All pre-existing diseases for first 48 months
- Dental treatments
- Cosmetic procedures
- Alternative treatments
- High-risk sports injuries

Network Hospitals:
- 3000+ hospitals across India
- 80+ cities covered
    
Suitable For:
- Young individuals under 35
- Basic coverage needs
- Budget-conscious customers"""
    
    c = canvas.Canvas("sample_policies/policy3.pdf", pagesize=letter)
    y = 750
    for line in pdf_content.split('\n'):
        if y < 50:
            c.showPage()
            y = 750
        c.drawString(50, y, line)
        y -= 20
    c.save()
    print("✅ Created sample_policies/policy3.pdf")
    
except ImportError:
    print("⚠️ reportlab not installed. Skipping PDF creation.")
    print("   Install with: pip install reportlab")
    print("   Or use an existing PDF file")
    
print("\n📁 Sample policies created in 'sample_policies/' folder:")
print("  - policy1.txt (Text format)")
print("  - policy2.json (JSON format)")
print("  - policy3.pdf (PDF format)")