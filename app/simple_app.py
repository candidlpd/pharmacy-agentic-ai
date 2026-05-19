"""
Simple Eli Lilly Pharmacy AI App - Test Version
Run: streamlit run app\simple_app.py
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import uuid

st.set_page_config(page_title="Eli Lilly Pharmacy AI", page_icon="💊", layout="wide")

st.title("💊 Eli Lilly Enterprise Pharmacy AI Platform")
st.markdown("*Multi-Agent System Test Version*")

# Initialize session state
if "cases" not in st.session_state:
    st.session_state.cases = []
if "case_count" not in st.session_state:
    st.session_state.case_count = 0

# Sidebar
with st.sidebar:
    st.header("🤖 System Status")
    st.metric("Cases Processed", st.session_state.case_count)
    st.markdown("---")
    st.subheader("Agent Flow")
    st.caption("1️⃣ Intake → 2️⃣ Drug Info → 3️⃣ Coverage → 4️⃣ Safety → 5️⃣ Decision")

# Main tabs
tab1, tab2 = st.tabs(["📝 New Case", "📊 Case History"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Patient Information")
        patient_name = st.text_input("Patient Name", "John Smith")
        allergies = st.text_input("Allergies (comma separated)", "None")
        conditions = st.text_input("Conditions", "Type 2 Diabetes")
    
    with col2:
        st.subheader("Prescription")
        drug = st.selectbox("Drug", ["trulicity", "mounjaro", "humalog", "ozempic"])
        dose = st.text_input("Dose", "0.75 mg")
        frequency = st.selectbox("Frequency", ["once weekly", "daily", "twice daily"])
        indication = st.text_input("Indication", "Type 2 Diabetes")
    
    if st.button("🚀 Process Case", type="primary"):
        # Simulate multi-agent processing
        with st.spinner("Processing with 5 agents..."):
            import time
            time.sleep(1)  # Simulate processing
            
            # Simulated responses
            drug_info = {
                "trulicity": {
                    "indications": ["Type 2 Diabetes"],
                    "standard_dose": "0.75 mg once weekly",
                    "max_dose": "4.5 mg once weekly",
                    "warnings": ["Pancreatitis", "Hypoglycemia"]
                },
                "mounjaro": {
                    "indications": ["Type 2 Diabetes"],
                    "standard_dose": "2.5 mg once weekly",
                    "max_dose": "15 mg once weekly",
                    "warnings": ["Severe GI issues"]
                },
                "humalog": {
                    "indications": ["Type 1", "Type 2 Diabetes"],
                    "standard_dose": "Individualized",
                    "max_dose": "Individualized",
                    "warnings": ["Hypoglycemia"]
                }
            }
            
            drug_data = drug_info.get(drug.lower(), drug_info["trulicity"])
            
            # Simulate decision
            approved = drug.lower() in ["trulicity", "mounjaro", "humalog"]
            risk_score = 0.2 if approved else 0.8
            
            case = {
                "case_id": str(uuid.uuid4())[:8],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "patient": patient_name,
                "drug": drug,
                "dose": dose,
                "drug_info": drug_data,
                "approved": approved,
                "risk_score": risk_score,
                "reason": "All criteria met" if approved else "Requires additional review"
            }
            
            st.session_state.cases.append(case)
            st.session_state.case_count += 1
        
        if approved:
            st.balloons()
            st.success(f"### ✅ APPROVED\n\n{case['reason']}")
            st.info(f"**Risk Score:** {risk_score:.0%}")
        else:
            st.warning(f"### ⚠️ REVIEW NEEDED\n\n{case['reason']}")
        
        # Show drug info
        with st.expander("📋 Drug Information", expanded=True):
            st.json(drug_data)

with tab2:
    if st.session_state.cases:
        df = pd.DataFrame(st.session_state.cases)
        st.dataframe(df, use_container_width=True)
        
        # Download button
        st.download_button(
            "Download Cases (JSON)",
            data=json.dumps(st.session_state.cases, indent=2),
            file_name="pharmacy_cases.json"
        )
    else:
        st.info("No cases processed yet. Go to 'New Case' tab.")

st.markdown("---")
st.caption("Built with Streamlit | Multi-Agent Architecture | Demo Version")