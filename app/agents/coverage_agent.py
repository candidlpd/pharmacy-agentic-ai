"""
COVERAGE AGENT - Agent 3 of 6
Checks insurance coverage and prior authorization
"""

from datetime import datetime

from ..state import CaseState, CoverageInfo


class CoverageAgent:
    """Third agent - checks insurance coverage"""
    
    def __init__(self):
        self.name = "CoverageAgent"
        
        self.coverage_data = {
            "trulicity": {"tier": 2, "pa_required": True, "copay": "$60"},
            "mounjaro": {"tier": 2, "pa_required": True, "copay": "$60"},
            "ozempic": {"tier": 2, "pa_required": True, "copay": "$60"},
            "humalog": {"tier": 1, "pa_required": False, "copay": "$25"}
        }
    
    def process(self, state: CaseState) -> CaseState:
        start_time = datetime.now()
        drug = state.order.drug.lower()
        
        data = self.coverage_data.get(drug, {"tier": 2, "pa_required": True, "copay": "$60"})
        
        state.coverage_info = CoverageInfo(
            tier=data["tier"],
            pa_required=data["pa_required"],
            copay=data["copay"]
        )
        
        state.status = "coverage_checked"
        
        latency = (datetime.now() - start_time).total_seconds() * 1000
        
        state.add_audit(
            self.name,
            "coverage_checked",
            {"drug": drug, "tier": data["tier"], "pa_required": data["pa_required"], "latency_ms": latency}
        )
        
        return state