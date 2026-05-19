"""
MAIN STREAMLIT APPLICATION
Run: streamlit run app/main_streamlit.py
"""

import streamlit as st
import pandas as pd
import json
import uuid
from datetime import datetime

from .state import CaseState, Patient, MedicationOrder
from .agents.intake_agent import IntakeAgent
from .agents.drug_agent import DrugAgent
from .agents.coverage_agent import CoverageAgent
from .agents.safety_agent import SafetyAgent
from .agents.risk_agent import RiskAgent
from .agents.decision_agent import DecisionAgent

# Page config
st.set_page_config(
    page_title="Eli Lilly Pharmacy AI",
    page_icon="💊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a5f7a 0%, #0d3b4f 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)


def run_agents(state: CaseState) -> CaseState:
    """Run all 6 agents in sequence"""
    
    agents = [
        IntakeAgent(),
        DrugAgent(),
        CoverageAgent(),
        SafetyAgent(),
        RiskAgent(),
        DecisionAgent()
    ]
    
    for agent in agents:
        state = agent.process(state)
        if state.status == "error":
            break
    
    return state


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💊 Eli Lilly Enterprise Pharmacy AI</h1>
        <p>Production Multi-Agent System | 6 Specialized Agents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Agent Status
    with st.sidebar:
        st.header("🤖 Agent System")
        agents_list = [
            "1️⃣ Intake Agent",
            "2️⃣ Drug Info Agent",
            "3️⃣ Coverage Agent",
            "4️⃣ Safety Agent",
            "5️⃣ Risk Agent",
            "6️⃣ Decision Agent"
        ]
        for agent in agents_list:
            st.caption(f"✅ {agent}")
        
        st.markdown("---")
        st.caption("Agent Flow: Intake → Drug → Coverage → Safety → Risk → Decision")
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📝 New Case", "📊 Agent Outputs", "📜 Case History"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Patient Information")
            patient_name = st.text_input("Patient Name", "John Smith")
            allergies = st.text_input("Allergies (comma separated)", "None")
            conditions = st.text_input("Medical Conditions", "Type 2 Diabetes")
            
        with col2:
            st.subheader("💊 Prescription")
            drug = st.selectbox("Drug", ["trulicity", "mounjaro", "humalog", "ozempic"])
            dose = st.text_input("Dose", "0.75 mg")
            frequency = st.selectbox("Frequency", ["once weekly", "daily"])
            indication = st.text_input("Indication", "Type 2 Diabetes")
        
        if st.button("🚀 Run Multi-Agent System", type="primary", use_container_width=True):
            # Parse allergies
            allergy_list = [a.strip() for a in allergies.split(",") if a.strip() and a.strip() != "None"]
            
            patient = Patient(name=patient_name, allergies=allergy_list, conditions=[conditions])
            order = MedicationOrder(drug=drug, dose=dose, frequency=frequency, indication=indication)
            
            state = CaseState(
                case_id=str(uuid.uuid4())[:8],
                patient=patient,
                order=order
            )
            
            with st.spinner("Running 6 agents in sequence..."):
                result = run_agents(state)
                st.session_state["current_case"] = result
                
                if "case_history" not in st.session_state:
                    st.session_state.case_history = []
                st.session_state.case_history.append(result.to_dict())
            
            # Show decision
            if result.decision.approved:
                st.balloons()
                st.success(f"### ✅ DECISION: APPROVED\n\n{result.decision.reason}")
            else:
                st.warning(f"### ⚠️ DECISION: REVIEW NEEDED\n\n{result.decision.reason}")
            
            # Show risk score
            risk = result.risk_assessment.risk_score
            if risk > 0.6:
                st.error(f"**Risk Score:** {risk:.0%} (HIGH Risk)")
            elif risk > 0.3:
                st.warning(f"**Risk Score:** {risk:.0%} (MEDIUM Risk)")
            else:
                st.info(f"**Risk Score:** {risk:.0%} (LOW Risk)")
            
            if result.decision.requires_hitl:
                st.info("👤 **Human-in-the-Loop:** This case requires human review.")
    
    with tab2:
        if "current_case" in st.session_state:
            case = st.session_state["current_case"]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Risk Score", f"{case.risk_assessment.risk_score:.0%}")
            with col2:
                st.metric("Decision", "✅ Approved" if case.decision.approved else "⚠️ Review")
            with col3:
                st.metric("PA Required", "Yes" if case.coverage_info.pa_required else "No")
            
            with st.expander("📋 Drug Info Agent", expanded=True):
                st.json(case.drug_info.to_dict())
            
            with st.expander("🛡️ Coverage Agent"):
                st.json(case.coverage_info.to_dict())
            
            with st.expander("⚠️ Safety Agent"):
                st.json(case.safety_info.to_dict())
            
            with st.expander("📊 Risk Agent"):
                st.json(case.risk_assessment.to_dict())
            
            with st.expander("🎯 Decision Agent"):
                st.json(case.decision.to_dict())
        else:
            st.info("No case processed yet. Go to 'New Case' tab.")
    
    with tab3:
        if "case_history" in st.session_state and st.session_state.case_history:
            df = pd.DataFrame(st.session_state.case_history)
            st.dataframe(df, use_container_width=True)
            
            st.download_button(
                "📥 Download Case History",
                data=json.dumps(st.session_state.case_history, indent=2),
                file_name="case_history.json"
            )
        else:
            st.info("No cases processed yet.")


if __name__ == "__main__":
    if "case_history" not in st.session_state:
        st.session_state.case_history = []
    main()