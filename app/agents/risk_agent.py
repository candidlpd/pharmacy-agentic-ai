"""
RISK AGENT - Agent 5 of 6
Calculates risk score based on all factors
"""

from datetime import datetime

from ..state import CaseState, RiskAssessment


class RiskAgent:
    """Fifth agent - calculates risk score"""
    
    def __init__(self):
        self.name = "RiskAgent"
    
    def process(self, state: CaseState) -> CaseState:
        start_time = datetime.now()
        
        risk_score = 0.0
        factors = []
        
        # Safety flags increase risk
        if state.safety_info.safety_flags:
            risk_score += 0.2
            factors.append("Safety flags present")
        
        # Dose issues
        if not state.safety_info.dose_ok:
            risk_score += 0.3
            factors.append("Dose exceeds maximum")
        
        # Allergies
        if state.safety_info.allergy_warnings:
            risk_score += 0.2
            factors.append("Allergy warnings")
        
        # Prior authorization
        if state.coverage_info.pa_required:
            risk_score += 0.1
            factors.append("PA required")
        
        # Cap at 1.0
        risk_score = min(1.0, risk_score)
        
        # Determine risk level
        if risk_score > 0.6:
            risk_level = "HIGH"
        elif risk_score > 0.3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        state.risk_assessment = RiskAssessment(
            risk_score=risk_score,
            risk_level=risk_level
        )
        
        state.status = "risk_assessed"
        
        latency = (datetime.now() - start_time).total_seconds() * 1000
        
        state.add_audit(
            self.name,
            "risk_assessed",
            {"risk_score": risk_score, "risk_level": risk_level, "factors": factors, "latency_ms": latency}
        )
        
        return state