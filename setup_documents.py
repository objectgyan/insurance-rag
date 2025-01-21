# setup_documents.py
from pathlib import Path
from datetime import datetime

def setup_test_documents():
    # Create documents directory
    docs_dir = Path("examples/sample_docs")
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Health Policy Content
    health_policy = """
HEALTH INSURANCE POLICY
Policy Number: HEALTH-2025-001
Date: 2025-01-20 22:18:11
Insured: objectgyan

PRIMARY COVERAGE DETAILS:
1. Primary Care Visits
   - Copay: $25 per visit
   - Annual check-up: Covered 100%
   - Preventive care: No copay

2. Specialist Care
   - Copay: $40 per visit
   - Referral required from primary care
   - Virtual consultation: $20 copay

3. Prescription Drug Coverage
   - Generic medications: $10 copay
   - Brand name medications: $30 copay
   - Specialty medications: 20% coinsurance
   - Mail order (90-day supply): 2x copay

4. Hospital Services
   - Inpatient care: $250 per day copay
   - Outpatient surgery: $150 copay
   - Emergency room: $200 copay (waived if admitted)
   - Urgent care: $50 copay

5. Mental Health Services
   - In-network therapy: $25 copay
   - Virtual mental health: $15 copay
   - Inpatient mental health: Same as medical

ADDITIONAL BENEFITS:
- Annual deductible: $1,000 individual/$2,000 family
- Out-of-pocket maximum: $3,000 individual/$6,000 family
- Wellness program discounts
- 24/7 Nurse hotline: 1-800-NURSE-24

HOW TO ACCESS CARE:
1. Find a provider: www.healthpolicy.com/providers
2. Virtual care: Download HealthApp or visit www.healthpolicy.com/virtual
3. Emergency: Call 911 or go to nearest emergency room
4. Questions: Call 1-800-HEALTH-1 (Available 24/7)
"""

    # Auto Policy Content
    auto_policy = """
AUTO INSURANCE POLICY
Policy Number: AUTO-2025-001
Date: 2025-01-20 22:18:11
Insured: objectgyan

COVERAGE DETAILS:
1. Collision Coverage
   - Deductible: $500
   - Coverage limit: $25,000

2. Comprehensive Coverage
   - Deductible: $250
   - Coverage limit: $25,000

3. Liability Coverage
   - Bodily Injury: $100,000 per person/$300,000 per accident
   - Property Damage: $50,000 per accident

Claims Process:
- Phone: 1-800-555-CLAIM
- Online: www.example.com/claims
- Mobile App: InsuranceApp
"""

    # Save Health Policy
    health_policy_path = docs_dir / "health_policy.txt"
    health_policy_path.write_text(health_policy)
    print(f"Created health policy at: {health_policy_path}")

    # Save Auto Policy
    auto_policy_path = docs_dir / "auto_policy.txt"
    auto_policy_path.write_text(auto_policy)
    print(f"Created auto policy at: {auto_policy_path}")

if __name__ == "__main__":
    print("Setting up test documents...")
    setup_test_documents()
    print("Setup complete!")