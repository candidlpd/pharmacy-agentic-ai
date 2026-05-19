"""
CREATE SAMPLE DATA
Run this first to create sample PDFs and database
"""

import sqlite3
import os
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PDFS_DIR = DATA_DIR / "pdfs"
DATABASE_DIR = DATA_DIR / "database"

# Create directories
PDFS_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 50)
print("Creating Sample Data for Eli Lilly Agentic AI")
print("=" * 50)

# ============================================
# 1. Create Sample Drug Label (Trulicity)
# ============================================
trulicity_label = """
TRULICITY (dulaglutide) Injection, for subcutaneous use

INDICATIONS AND USAGE:
Trulicity is indicated as an adjunct to diet and exercise to improve glycemic control 
in adults with type 2 diabetes mellitus.

DOSAGE AND ADMINISTRATION:
- Starting dose: 0.75 mg once weekly
- May increase to 1.5 mg once weekly after 4 weeks
- Maximum dose: 4.5 mg once weekly

CONTRAINDICATIONS:
- Personal or family history of medullary thyroid carcinoma (MTC)
- Multiple Endocrine Neoplasia syndrome type 2 (MEN 2)

WARNINGS AND PRECAUTIONS:
- Risk of pancreatitis
- Hypoglycemia when used with insulin or sulfonylureas
- Acute kidney injury

ADVERSE REACTIONS:
- Nausea (21%)
- Diarrhea (13%)
- Vomiting (9%)
- Abdominal pain (7%)
"""

with open(PDFS_DIR / "trulicity_label.txt", "w") as f:
    f.write(trulicity_label)
print("✓ Created: data/pdfs/trulicity_label.txt")

# ============================================
# 2. Create Sample Database
# ============================================
db_path = DATABASE_DIR / "pharmacy.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Create drugs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS drugs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    generic_name TEXT,
    manufacturer TEXT,
    tier INTEGER,
    pa_required INTEGER,
    step_therapy INTEGER,
    copay_amount REAL
)
""")

# Insert sample data
drugs = [
    (1, "trulicity", "dulaglutide", "Eli Lilly", 2, 1, 1, 60.00),
    (2, "mounjaro", "tirzepatide", "Eli Lilly", 2, 1, 1, 60.00),
    (3, "ozempic", "semaglutide", "Novo Nordisk", 2, 1, 1, 60.00),
    (4, "humalog", "insulin lispro", "Eli Lilly", 1, 0, 0, 25.00),
    (5, "metformin", "metformin HCl", "Various", 1, 0, 0, 10.00)
]

cursor.executemany("INSERT OR REPLACE INTO drugs VALUES (?,?,?,?,?,?,?,?)", drugs)

conn.commit()
conn.close()
print(f"✓ Created database: {db_path}")
print("  - Table: drugs (5 rows)")

# ============================================
# 3. Create Sample Case
# ============================================
import json
sample_case = {
    "case_id": "SAMPLE_001",
    "patient": {
        "name": "John Smith",
        "allergies": ["None"],
        "conditions": ["Type 2 Diabetes"],
        "age": 52
    },
    "order": {
        "drug": "trulicity",
        "dose": "0.75 mg",
        "frequency": "once weekly",
        "indication": "Type 2 Diabetes"
    }
}

cases_dir = DATA_DIR / "cases"
cases_dir.mkdir(exist_ok=True)

with open(cases_dir / "sample_case.json", "w") as f:
    json.dump(sample_case, f, indent=2)
print(f"✓ Created: data/cases/sample_case.json")

print("\n" + "=" * 50)
print("SAMPLE DATA CREATION COMPLETE!")
print("=" * 50)
print("\nNext steps:")
print("1. Run: python scripts/build_index.py")
print("2. Run: streamlit run app/main_streamlit.py")