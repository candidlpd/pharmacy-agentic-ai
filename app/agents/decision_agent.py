"""
DECISION AGENT - Agent 6 of 6
Makes final approval decision
"""

from datetime import datetime

from ..state import CaseState, Decision
from ..config import HIGH_RISK_THRESHOLD, HITL_THRESHOLD


class DecisionAgent:
    """Sixth agent - makes final decision"""
    
    def __init__(self):
        self.name = "DecisionAgent"
    
    def process(self, state: CaseState) -> CaseState:
        start_time = datetime.now()
        
        approved = True
        reasons = []
        
        # Check risk score
        if state.risk_assessment.risk_score > HIGH_RISK_THRESHOLD:
            approved = False
            reasons.append(f"Risk score too high ({state.risk_assessment.risk_score:.0%})")
        
        # Check dose safety
        if not state.safety_info.dose_ok:
            approved = False
            reasons.append("Dose exceeds maximum recommendation")
        
        # Check allergies
        if state.safety_info.allergy_warnings:
            approved = False
            reasons.extend(state.safety_info.allergy_warnings)
        
        # If no issues, approve
        if not reasons:
            reasons.append("All safety and coverage criteria met")
        
        # Determine if HITL required
        requires_hitl = not approved or state.risk_assessment.risk_score > HITL_THRESHOLD
        
        state.decision = Decision(
            approved=approved,
            reason="; ".join(reasons),
            requires_hitl=requires_hitl
        )
        
        state.status = "completed" if approved else "hitl_required"
        
        latency = (datetime.now() - start_time).total_seconds() * 1000
        
        state.add_audit(
            self.name,
            "decision_made",
            {"approved": approved, "requires_hitl": requires_hitl, "reason": reasons[0], "latency_ms": latency}
        )
        
        return state