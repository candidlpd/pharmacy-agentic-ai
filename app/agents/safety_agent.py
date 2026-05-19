"""
SAFETY AGENT - Agent 4 of 6
Checks dose safety, allergies, interactions
"""

import re
from datetime import datetime

from ..state import CaseState, SafetyInfo


class SafetyAgent:
    """Fourth agent - checks safety"""
    
    def __init__(self):
        self.name = "SafetyAgent"
        
        self.max_doses = {
            "trulicity": 4.5,
            "mounjaro": 15.0,
            "ozempic": 2.0
        }
    
    def process(self, state: CaseState) -> CaseState:
        start_time = datetime.now()
        drug = state.order.drug.lower()
        
        # Check dose
        dose_num = self._extract_dose_number(state.order.dose)
        max_dose = self.max_doses.get(drug, 10)
        dose_ok = dose_num <= max_dose if max_dose else True
        
        # Check allergies
        allergy_warnings = []
        if state.patient.allergies:
            for allergy in state.patient.allergies:
                if allergy.lower() in ["glp-1", "liraglutide"]:
                    allergy_warnings.append(f"Potential reaction to {allergy}")
        
        # Get safety flags from drug info
        safety_flags = state.drug_info.warnings.copy()
        
        state.safety_info = SafetyInfo(
            dose_ok=dose_ok,
            allergy_warnings=allergy_warnings,
            safety_flags=safety_flags
        )
        
        state.status = "safety_checked"
        
        latency = (datetime.now() - start_time).total_seconds() * 1000
        
        state.add_audit(
            self.name,
            "safety_checked",
            {"dose_ok": dose_ok, "allergy_warnings": len(allergy_warnings), "latency_ms": latency}
        )
        
        return state
    
    def _extract_dose_number(self, dose_str: str) -> float:
        match = re.search(r'(\d+\.?\d*)', dose_str)
        return float(match.group(1)) if match else 0