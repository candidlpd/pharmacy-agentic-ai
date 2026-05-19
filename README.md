# 💊 Pharmacy Agentic AI - Multi-Agent System for Pharmacy Automation

## A Complete AI System That Works Like a Team of 6 Pharmacy Specialists

---

# 📖 WHAT IS THIS PROJECT? (Explained Like You're 10)

## The Problem

When you go to a pharmacy with a prescription, a pharmacist must:

1. Read your prescription
2. Look up the drug in a medical book
3. Call your insurance company
4. Check if the drug is safe with your other medicines
5. Calculate if the dose is correct
6. Make a decision - approve or deny

This normally takes **30 minutes to several DAYS**.

---

## Our Solution

Instead of ONE person doing everything, we have **6 AI specialists** working like an assembly line:

```text
STEP 1: You type prescription
STEP 2: Agent 1 (Receptionist) → Checks your input
STEP 3: Agent 2 (Pharmacist) → Looks up drug information
STEP 4: Agent 3 (Insurance) → Checks insurance coverage
STEP 5: Agent 4 (Safety Officer) → Checks dose and allergies
STEP 6: Agent 5 (Risk Calculator) → Calculates risk score
STEP 7: Agent 6 (Manager) → Makes final decision
STEP 8: DONE in 2 SECONDS!
```

---

# 🧠 WHAT MAKES THIS "AGENTIC AI"?

| Regular Chatbot | Agentic AI |
|---|---|
| One AI does everything | Multiple specialized AI agents |
| General answers | Specialized expert behavior |
| No actions | Takes actions |
| No workflow | Sequential orchestration |
| No memory/state | Shared state |
| No explainability | Full audit trail |

---

# 🤖 THE 6 AGENTS

## 1. Intake Agent — "Receptionist"

### Responsibilities
- Validate patient input
- Validate prescription
- Clean and normalize data
- Generate Case ID

### Example
```text
Input:
John Smith, Trulicity 0.75mg

Output:
Validated Case ID: CASE_001
```

---

## 2. Drug Information Agent — "Pharmacist"

### Responsibilities
- Retrieve drug information
- Check max dose
- Check warnings
- Check contraindications

### Reads From
```text
data/database/drugs.json
```

### Example
```json
{
  "name": "Trulicity",
  "max_dose": "4.5 mg",
  "warnings": ["Pancreatitis"]
}
```

---

## 3. Coverage Agent — "Insurance Specialist"

### Responsibilities
- Check formulary tier
- Check copay
- Check Prior Authorization
- Check insurance rules

### Example
```text
Tier: 2
Copay: $60
PA Required: YES
```

---

## 4. Safety Agent — "Safety Officer"

### Responsibilities
- Compare dose vs max dose
- Check allergies
- Check interactions
- Check safety warnings

### Example
```text
Prescribed Dose: 0.75mg
Maximum Dose: 4.5mg
Result: SAFE
```

---

## 5. Risk Agent — "Risk Calculator"

### Responsibilities
- Calculate risk score
- Determine LOW/MEDIUM/HIGH risk
- Escalate risky cases

### Risk Formula

```text
PA Required → +10
Warnings → +10
High Dose → +20
Allergies → +20
```

### Example
```text
Final Risk Score: 20
Risk Level: LOW
```

---

## 6. Decision Agent — "Manager"

### Responsibilities
- Make final decision
- Approve or reject
- Trigger HITL review if needed

### Rules

```text
Risk < 50 → APPROVED
Risk >= 50 → REVIEW NEEDED
```

---

# 🔄 COMPLETE MULTI-AGENT FLOW

```text
USER INPUT
   ↓
INTAKE AGENT
   ↓
DRUG AGENT
   ↓
COVERAGE AGENT
   ↓
SAFETY AGENT
   ↓
RISK AGENT
   ↓
DECISION AGENT
   ↓
FINAL OUTPUT
```

---

# 📁 PROJECT STRUCTURE

```text
pharmacy-agentic-ai/
│
├── app/
│   └── simple_working_app.py
│
├── data/
│   ├── database/
│   │   ├── drugs.json
│   │   ├── coverage_rules.json
│   │   └── safety_data.json
│   │
│   └── cases/
│       └── sample_cases.json
│
├── scripts/
│   └── create_sample_data.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📊 DATA FILES

## drugs.json

```json
{
  "name": "Trulicity",
  "dosing": {
    "maximum": "4.5 mg"
  },
  "tier": 2,
  "pa_required": true,
  "copay": "$60"
}
```

---

## coverage_rules.json

```json
{
  "Trulicity": {
    "prior_auth": true,
    "tier": 2,
    "copay": "$60"
  }
}
```

---

## safety_data.json

```json
{
  "Trulicity": {
    "max_weekly_mg": 4.5,
    "interactions": ["Insulin"]
  }
}
```

---

# 🚀 HOW TO RUN THE PROJECT

## Step 1 — Clone Repository

```bash
git clone https://github.com/candidlpd/pharmacy-agentic-ai.git
cd pharmacy-agentic-ai
```

---

## Step 2 — Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3 — Install Packages

```bash
pip install -r requirements.txt
```

---

## Step 4 — Create Sample Data

```bash
python scripts/create_sample_data.py
```

---

## Step 5 — Run Application

```bash
streamlit run app/simple_working_app.py
```

---

## Step 6 — Open Browser

```text
http://localhost:8501
```

---

# 🧪 TEST CASES

## Test Case 1 — APPROVED

| Field | Value |
|---|---|
| Drug | Trulicity |
| Dose | 0.75mg |
| Result | APPROVED |

---

## Test Case 2 — REVIEW NEEDED

| Field | Value |
|---|---|
| Drug | Trulicity |
| Dose | 6mg |
| Result | REVIEW NEEDED |

---

# 📊 RISK SCORE MEANING

| Score | Risk Level | Decision |
|---|---|---|
| 0-30 | LOW | APPROVED |
| 30-60 | MEDIUM | REVIEW |
| 60-100 | HIGH | HITL |

---

# 🎤 INTERVIEW EXPLANATION

## 30-Second Pitch

> "I built a production-style pharmacy agentic AI platform using 6 specialized AI agents working sequentially. Each agent performs one task such as validation, retrieval, safety analysis, insurance coverage, risk scoring, and final decisioning. The system automates pharmacy workflows and reduces approval time from days to seconds."

---

# 🏗️ ARCHITECTURE TYPE

```text
Sequential Specialized Multi-Agent Architecture
```

---

# 🧠 TECHNOLOGIES USED

| Technology | Purpose |
|---|---|
| Python | Backend |
| Streamlit | UI |
| JSON | Database |
| Multi-Agent AI | Workflow |
| Risk Scoring | Decision Intelligence |

---

# 📈 KEY METRICS

| Metric | Value |
|---|---|
| Agents | 6 |
| Processing Time | < 2 seconds |
| Risk Scoring | 0-100 |
| Human-in-the-loop | YES |
| Explainability | YES |

---

# 🏆 WHY THIS PROJECT IS IMPORTANT

✅ Real Agentic AI  
✅ Multi-Agent Workflow  
✅ Production Architecture  
✅ Human-in-the-loop  
✅ Explainable AI  
✅ Portfolio Ready  
✅ Interview Ready  

---

# 📄 LICENSE

Educational and portfolio purposes only.

---

# ⭐ GITHUB

```text
https://github.com/candidlpd/pharmacy-agentic-ai
```

---

# 🎉 FINAL RESULT

You now have:

✅ Multi-Agent AI System  
✅ Sequential Agent Workflow  
✅ Risk Scoring Engine  
✅ Explainable AI Pipeline  
✅ Production-Style Architecture  
✅ Interview-Ready Project  

🚀
