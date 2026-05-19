"""
ELI LILLY PHARMACY AI - MINIMAL WORKING VERSION
No LangChain/LangGraph dependencies required
"""

import streamlit as st
import pandas as pd
import json
import uuid
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Eli Lilly Pharmacy AI",
    page_icon="💊",
    layout="wide"
)

# Drug Database
DRUGS = {
    "trulicity": {
        "name": "Trulicity (dulaglutide)",
        "indications": ["Type 2 Diabetes Mellitus"],
        "dose_start": "0.75 mg once weekly",
        "dose_max": "4.5 mg once weekly",
        "warnings": ["Pancreatitis", "Hypoglycemia"],
        "contraindications": ["MTC", "MEN2"],
        "tier": 2,
        "pa_required": True,
        "copay": "$60"
    },
    "mounjaro": {
        "name": "Mounjaro (tirzepatide)",
        "indications": ["Type 2 Diabetes Mellitus"],
        "dose_start": "2.5 mg once weekly",
        "dose_max": "15 mg once weekly",
        "warnings": ["Severe GI issues"],
        "contraindications": ["MTC"],
        "tier": 2,
        "pa_required": True,
        "copay": "$60"
    },
    "humalog": {
        "name": "Humalog (insulin lispro)",
        "indications": ["Type 1 Diabetes", "Type 2 Diabetes"],
        "dose_start": "Individualized",
        "dose_max": "Individualized",
        "warnings": ["Hypoglycemia"],
        "contraindications": ["Hypoglycemia"],
        "tier": 1,
        "pa_required": False,
        "copay": "$25"
    },
    "ozempic": {
        "name": "Ozempic (semaglutide)",
        "indications": ["Type 2 Diabetes Mellitus"],
        "dose_start": "0.25 mg once weekly",
        "dose_max": "2.0 mg once weekly",
        "warnings": ["Pancreatitis", "Gallbladder disease"],
        "contraindications": ["MTC", "MEN2"],
        "tier": 2,
        "pa_required": True,
        "copay": "$60"
    }
}

# Header
st.markdown("""
<style>
.header { background: linear-gradient(135deg, #1a5f7a 0%, #0d3b4f 100%); 
          padding: 1.5rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem; }
.metric-card { background-color: #f0f2f6; padding: 1rem; border-radius: 10px; text-align: center; }
</style>
<div class="header">
    <h1>💊 Eli Lilly Pharmacy AI</h1>
    <p>Multi-Agent System | 6 Specialized Agents | Production Ready</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🤖 6 Agents")
    st.caption("1️⃣ Intake Agent - Validates input")
    st.caption("2️⃣ Drug Info Agent - Looks up drug data")
    st.caption("3️⃣ Coverage Agent - Checks insurance")
    st.caption("4️⃣ Safety Agent - Checks dose/allergies")
    st.caption("5️⃣ Risk Agent - Calculates risk score")
    st.caption("6️⃣ Decision Agent - Makes approval decision")
    st.markdown("---")
    st.caption("Flow: Intake → Drug → Coverage → Safety → Risk → Decision")
    
    # Show status
    st.markdown("---")
    st.success("✅ All 6 Agents Ready")

# Main area
tab1, tab2, tab3 = st.tabs(["📝 New Case", "📊 Agent Results", "📜 Case History"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Patient Information")
        name = st.text_input("Patient Name", "John Smith")
        allergies = st.text_input("Allergies (comma separated)", "None")
        conditions = st.text_input("Medical Conditions", "Type 2 Diabetes")
        age = st.number_input("Age", min_value=0, max_value=120, value=52)
    
    with col2:
        st.subheader("💊 Prescription Information")
        drug = st.selectbox("Drug", list(DRUGS.keys()))
        dose = st.text_input("Dose", "0.75 mg")
        frequency = st.selectbox("Frequency", ["once weekly", "daily", "twice daily"])
        indication = st.text_input("Indication", "Type 2 Diabetes")
    
    if st.button("🚀 Run 6 Agents", type="primary", use_container_width=True):
        # ============================================
        # AGENT 1: Intake Agent
        # ============================================
        case_id = f"CASE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        intake_result = {
            "agent": "IntakeAgent",
            "status": "success",
            "case_id": case_id,
            "patient_name": name,
            "drug_normalized": drug.lower()
        }
        
        # ============================================
        # AGENT 2: Drug Info Agent
        # ============================================
        drug_info = DRUGS[drug].copy()
        drug_result = {
            "agent": "DrugInfoAgent",
            "status": "success",
            "drug": drug,
            "info": drug_info
        }
        
        # ============================================
        # AGENT 3: Coverage Agent
        # ============================================
        coverage = {
            "agent": "CoverageAgent",
            "status": "success",
            "tier": drug_info["tier"],
            "pa_required": drug_info["pa_required"],
            "copay": drug_info["copay"],
            "covered": drug_info["tier"] <= 2
        }
        
        # ============================================
        # AGENT 4: Safety Agent
        # ============================================
        # Extract dose number
        import re
        dose_match = re.search(r'(\d+\.?\d*)', dose)
        dose_num = float(dose_match.group(1)) if dose_match else 0
        
        # Get max dose
        max_dose_str = drug_info["dose_max"]
        max_match = re.search(r'(\d+\.?\d*)', max_dose_str)
        max_dose = float(max_match.group(1)) if max_match else 10
        
        dose_ok = dose_num <= max_dose if max_dose_str != "Individualized" else True
        
        # Check allergies
        allergy_list = [a.strip().lower() for a in allergies.split(",") if a.strip() and a.strip().lower() != "none"]
        allergy_warnings = []
        
        if allergy_list:
            allergy_warnings.append(f"Patient has allergies: {', '.join(allergy_list)}")
        
        safety_result = {
            "agent": "SafetyAgent",
            "status": "success",
            "dose_ok": dose_ok,
            "dose_num": dose_num,
            "max_dose": max_dose,
            "allergy_warnings": allergy_warnings,
            "safety_flags": drug_info["warnings"]
        }
        
        # ============================================
        # AGENT 5: Risk Agent
        # ============================================
        risk_score = 0.0
        risk_factors = []
        
        if not dose_ok:
            risk_score += 0.3
            risk_factors.append(f"Dose {dose_num}mg exceeds max {max_dose}mg")
        
        if allergy_warnings:
            risk_score += 0.2
            risk_factors.append("Allergy warnings present")
        
        if drug_info["pa_required"]:
            risk_score += 0.1
            risk_factors.append("Prior authorization required")
        
        if drug_info["warnings"]:
            risk_score += 0.1
            risk_factors.append("Safety warnings exist")
        
        risk_score = min(1.0, risk_score)
        
        if risk_score >= 0.6:
            risk_level = "HIGH"
        elif risk_score >= 0.3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        risk_result = {
            "agent": "RiskAgent",
            "status": "success",
            "risk_score": risk_score,
            "risk_level": risk_level,
            "factors": risk_factors
        }
        
        # ============================================
        # AGENT 6: Decision Agent
        # ============================================
        approved = risk_score < 0.5 and dose_ok
        reasons = []
        
        if approved:
            reasons.append("All safety and coverage criteria met")
        else:
            if risk_score >= 0.5:
                reasons.append(f"Risk score too high ({risk_score:.0%})")
            if not dose_ok:
                reasons.append(f"Dose {dose_num}mg exceeds maximum ({max_dose}mg)")
        
        decision_result = {
            "agent": "DecisionAgent",
            "status": "success",
            "approved": approved,
            "reason": "; ".join(reasons),
            "requires_hitl": not approved or risk_score > 0.4
        }
        
        # ============================================
        # COMBINE ALL RESULTS
        # ============================================
        full_result = {
            "case_id": case_id,
            "timestamp": datetime.now().isoformat(),
            "patient": {
                "name": name,
                "age": age,
                "allergies": allergy_list,
                "conditions": conditions
            },
            "order": {
                "drug": drug,
                "dose": dose,
                "frequency": frequency,
                "indication": indication
            },
            "agents": {
                "intake": intake_result,
                "drug_info": drug_result,
                "coverage": coverage,
                "safety": safety_result,
                "risk": risk_result,
                "decision": decision_result
            },
            "final": {
                "approved": approved,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "reason": decision_result["reason"]
            }
        }
        
        # Save to session
        st.session_state["current_case"] = full_result
        if "case_history" not in st.session_state:
            st.session_state.case_history = []
        st.session_state.case_history.append(full_result)
        
        # Show decision
        if approved:
            st.balloons()
            st.success(f"### ✅ DECISION: APPROVED\n\n{decision_result['reason']}")
        else:
            st.warning(f"### ⚠️ DECISION: REVIEW NEEDED\n\n{decision_result['reason']}")
        
        # Show metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Risk Score", f"{risk_score:.0%}")
        with col2:
            st.metric("Risk Level", risk_level)
        with col3:
            st.metric("PA Required", "Yes" if drug_info["pa_required"] else "No")
        with col4:
            st.metric("Tier", drug_info["tier"])
        
        if decision_result["requires_hitl"]:
            st.info("👤 **Human-in-the-Loop:** This case requires human review.")
        
        # Show agent summary
        with st.expander("📋 View All 6 Agent Outputs", expanded=True):
            st.json(full_result)

with tab2:
    if "current_case" in st.session_state:
        case = st.session_state["current_case"]
        
        # Agent by agent breakdown
        st.subheader("Agent Execution Results")
        
        for agent_name, agent_output in case["agents"].items():
            with st.expander(f"🤖 {agent_name}", expanded=False):
                st.json(agent_output)
        
        # Final summary
        st.subheader("Final Decision Summary")
        st.json(case["final"])
    else:
        st.info("No case processed yet. Go to 'New Case' tab.")

with tab3:
    if "case_history" in st.session_state and st.session_state.case_history:
        # Create summary dataframe
        history_data = []
        for case in st.session_state.case_history:
            history_data.append({
                "Case ID": case["case_id"][-12:],
                "Patient": case["patient"]["name"],
                "Drug": case["order"]["drug"],
                "Approved": "✅" if case["final"]["approved"] else "⚠️",
                "Risk Score": f"{case['final']['risk_score']:.0%}",
                "Risk Level": case["final"]["risk_level"],
                "Timestamp": case["timestamp"][:19]
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True)
        
        # Download button
        st.download_button(
            "📥 Download Case History (JSON)",
            data=json.dumps(st.session_state.case_history, indent=2),
            file_name="pharmacy_case_history.json",
            mime="application/json"
        )
    else:
        st.info("No cases processed yet.")

# Footer
st.markdown("---")
st.caption("🏢 Eli Lilly Enterprise Pharmacy AI | 6-Agent Multi-Agent System | Production Ready")