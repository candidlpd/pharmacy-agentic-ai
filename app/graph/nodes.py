"""
LangGraph Nodes - Each node is an agent that processes state
Uses LangChain for LLM operations and tools
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from ..state import CaseState
from ..chains.drug_chain import drug_chain
from ..chains.coverage_chain import coverage_chain
from ..chains.safety_chain import safety_chain
from ..tools.retrieval_tool import get_retrieval_tool
from ..evaluation.ragas_eval import evaluate_response

# ============================================
# NODE 1: Intake Agent
# ============================================
async def intake_node(state: CaseState) -> Dict[str, Any]:
    """
    Validate and normalize incoming case data
    """
    # Validate required fields
    if not state.order.drug:
        return {"error": "Drug name required", "status": "error"}
    
    # Normalize drug name
    state.order.drug = state.order.drug.lower().strip()
    
    # Generate trace ID
    import uuid
    state.trace_id = str(uuid.uuid4())
    
    state.current_step = "intake_complete"
    
    return {
        "case_id": state.case_id,
        "order": state.order,
        "trace_id": state.trace_id,
        "current_step": "intake_complete"
    }

# ============================================
# NODE 2: Retrieval Agent (LangChain Tool)
# ============================================
async def retrieval_node(state: CaseState) -> Dict[str, Any]:
    """
    Retrieve relevant documents using LangChain Retrieval Tool
    """
    retrieval_tool = get_retrieval_tool()
    
    query = f"{state.order.drug} {state.order.indication} {state.question}"
    
    # Use LangChain's tool interface
    result = await retrieval_tool.ainvoke({
        "query": query,
        "k": 5
    })
    
    state.retrieved_documents = result.get("documents", [])
    
    return {
        "retrieved_documents": state.retrieved_documents,
        "current_step": "retrieval_complete"
    }

# ============================================
# NODE 3: Drug Info Agent (LangChain Chain)
# ============================================
async def drug_node(state: CaseState) -> Dict[str, Any]:
    """
    Get drug information using LangChain chain
    """
    # Use the drug chain (defined separately)
    response = await drug_chain.ainvoke({
        "drug": state.order.drug,
        "indication": state.order.indication,
        "context": state.retrieved_documents
    })
    
    state.drug_response = response.get("answer", "")
    state.citations = response.get("citations", [])
    
    return {
        "drug_response": state.drug_response,
        "citations": state.citations,
        "current_step": "drug_complete"
    }

# ============================================
# NODE 4: Coverage Agent
# ============================================
async def coverage_node(state: CaseState) -> Dict[str, Any]:
    """
    Check insurance coverage using LangChain chain
    """
    response = await coverage_chain.ainvoke({
        "drug": state.order.drug,
        "context": state.retrieved_documents
    })
    
    state.coverage_response = response.get("coverage_status", "")
    state.prior_auth_required = response.get("pa_required", False)
    
    return {
        "coverage_response": state.coverage_response,
        "current_step": "coverage_complete"
    }

# ============================================
# NODE 5: Safety Agent
# ============================================
async def safety_node(state: CaseState) -> Dict[str, Any]:
    """
    Check drug safety using LangChain chain
    """
    response = await safety_chain.ainvoke({
        "drug": state.order.drug,
        "dose": state.order.dose,
        "patient_allergies": state.patient.allergies,
        "context": state.retrieved_documents
    })
    
    state.safety_response = response.get("safety_status", "")
    state.safety_flags = response.get("flags", [])
    
    return {
        "safety_response": state.safety_response,
        "safety_flags": state.safety_flags,
        "current_step": "safety_complete"
    }

# ============================================
# NODE 6: Compliance Agent
# ============================================
async def compliance_node(state: CaseState) -> Dict[str, Any]:
    """
    Check regulatory compliance
    """
    compliance_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a pharmacy compliance officer. Check if the following is compliant with FDA regulations."),
        ("human", "Drug: {drug}\nIndication: {indication}\nIs this off-label?")
    ])
    
    from ..config import settings
    from langchain_community.llms import Ollama
    llm = Ollama(model=settings.OLLAMA_MODEL)
    
    chain = compliance_prompt | llm | StrOutputParser()
    
    result = await chain.ainvoke({
        "drug": state.order.drug,
        "indication": state.order.indication
    })
    
    state.compliance_response = result
    
    return {"compliance_response": state.compliance_response}

# ============================================
# NODE 7: Risk Assessment Agent
# ============================================
async def risk_node(state: CaseState) -> Dict[str, Any]:
    """
    Calculate risk score based on all factors
    """
    risk_score = 0.0
    
    # Safety flags increase risk
    if state.safety_flags:
        risk_score += min(0.5, len(state.safety_flags) * 0.1)
    
    # Prior auth increases risk
    if getattr(state, 'prior_auth_required', False):
        risk_score += 0.2
    
    # Off-label increases risk
    if "off-label" in state.compliance_response.lower():
        risk_score += 0.3
    
    state.risk_score = min(1.0, risk_score)
    
    return {"risk_score": state.risk_score}

# ============================================
# NODE 8: Evaluation Agent (RAGAS + TruLens)
# ============================================
async def evaluation_node(state: CaseState) -> Dict[str, Any]:
    """
    Evaluate response quality using RAGAS framework
    """
    # Build the complete answer
    state.final_answer = f"""
    Drug Information: {state.drug_response}
    Coverage: {state.coverage_response}
    Safety: {state.safety_response}
    """
    
    # Use RAGAS for evaluation
    metrics = await evaluate_response(
        question=f"{state.order.drug} {state.order.indication}",
        answer=state.final_answer,
        contexts=[doc.get("text", "") for doc in state.retrieved_documents]
    )
    
    state.evaluation_metrics = metrics
    
    return {"evaluation_metrics": metrics, "final_answer": state.final_answer}

# ============================================
# NODE 9: Decision Agent
# ============================================
async def decision_node(state: CaseState) -> Dict[str, Any]:
    """
    Make final approval decision
    """
    approved = False
    reason = []
    
    # Check evaluation metrics
    if state.evaluation_metrics.faithfulness > 0.7:
        approved = True
        reason.append("High faithfulness score")
    else:
        reason.append("Low faithfulness score")
    
    # Check risk score
    if state.risk_score > 0.5:
        approved = False
        reason.append(f"Risk score too high ({state.risk_score})")
    
    # Check safety
    if state.safety_flags:
        approved = False
        reason.append(f"Safety flags: {', '.join(state.safety_flags)}")
    
    state.approved = approved
    state.decision_reason = "; ".join(reason)
    state.status = "completed" if approved else "hitl_required"
    
    return {
        "approved": approved,
        "decision_reason": state.decision_reason,
        "status": state.status
    }