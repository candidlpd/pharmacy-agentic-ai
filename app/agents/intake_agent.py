"""
INTAKE AGENT - Agent 1 of 6
Validates and normalizes incoming case data
"""

import uuid
from datetime import datetime
from typing import Dict

from ..state import CaseState


class IntakeAgent:
    """First agent - validates and normalizes input"""
    
    def __init__(self):
        self.name = "IntakeAgent"
    
    def process(self, state: CaseState) -> CaseState:
        start_time = datetime.now()
        
        # Generate case ID
        if not state.case_id:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            state.case_id = f"PHARM_{timestamp}"
        
        # Normalize drug name
        if state.order.drug:
            state.order.drug = state.order.drug.lower().strip()
        
        # Validate required fields
        errors = []
        if not state.patient.name:
            errors.append("Patient name required")
        if not state.order.drug:
            errors.append("Drug name required")
        
        if errors:
            state.status = "error"
            state.error_message = "; ".join(errors)
        else:
            state.status = "intake_complete"
        
        latency = (datetime.now() - start_time).total_seconds() * 1000
        
        state.add_audit(
            self.name,
            "intake_complete",
            {"case_id": state.case_id, "drug": state.order.drug, "latency_ms": latency}
        )
        
        return state