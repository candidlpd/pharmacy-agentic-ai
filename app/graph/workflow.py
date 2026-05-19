"""
Main LangGraph Workflow - Production-grade agent orchestration
Uses LangGraph for state management and conditional routing
"""

from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver
from langgraph.prebuilt import ToolExecutor

from ..state import CaseState
from .nodes import (
    intake_node,
    retrieval_node,
    drug_node,
    coverage_node,
    safety_node,
    compliance_node,
    risk_node,
    evaluation_node,
    decision_node
)

# ============================================
# BUILD THE LANGGRAPH WORKFLOW
# ============================================

def build_pharmacy_graph() -> StateGraph:
    """
    Build the complete LangGraph workflow for pharmacy operations.
    This defines the orchestration of all agents.
    """
    
    # Create the graph with the state schema
    workflow = StateGraph(CaseState)
    
    # ========== ADD NODES (Agents) ==========
    workflow.add_node("intake", intake_node)
    workflow.add_node("retrieve", retrieval_node)
    workflow.add_node("drug_info", drug_node)
    workflow.add_node("coverage", coverage_node)
    workflow.add_node("safety", safety_node)
    workflow.add_node("compliance", compliance_node)
    workflow.add_node("risk_assessment", risk_node)
    workflow.add_node("evaluation", evaluation_node)
    workflow.add_node("decision", decision_node)
    
    # ========== SET ENTRY POINT ==========
    workflow.set_entry_point("intake")
    
    # ========== ADD EDGES (Sequential Flow) ==========
    workflow.add_edge("intake", "retrieve")
    workflow.add_edge("retrieve", "drug_info")
    workflow.add_edge("drug_info", "coverage")
    workflow.add_edge("coverage", "safety")
    workflow.add_edge("safety", "compliance")
    workflow.add_edge("compliance", "risk_assessment")
    workflow.add_edge("risk_assessment", "evaluation")
    
    # ========== CONDITIONAL EDGE (Decision) ==========
    def should_approve(state: CaseState) -> Literal["decision", "hitl"]:
        """Conditional routing based on risk score"""
        if state.risk_score > 0.7:
            return "hitl"  # Needs human review
        return "decision"  # Auto-approve
    
    workflow.add_conditional_edges(
        "evaluation",
        should_approve,
        {
            "decision": "decision",
            "hitl": END  # End with HITL required
        }
    )
    
    workflow.add_edge("decision", END)
    
    # ========== COMPILE GRAPH ==========
    # Add memory saver for production checkpointing
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    return app

# Create the global graph instance
pharmacy_graph = build_pharmacy_graph()