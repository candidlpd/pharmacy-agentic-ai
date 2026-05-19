"""
DRUG INFO AGENT - Agent 2 of 6
Retrieves drug information from database
"""

from datetime import datetime
from typing import Dict

from ..state import CaseState, DrugInfo


class DrugAgent:
    """Second agent - retrieves drug information"""
    
    def __init__(self):
        self.name = "DrugAgent"
        
        # Drug database
        self.drug_data = {
            "trulicity": {
                "indications": ["Type 2 Diabetes Mellitus"],
                "standard_dose": "0.75 mg once weekly",
                "max_dose": "4.5 mg once weekly",
                "warnings": ["Pancreatitis", "Hypoglycemia"],
                "contraindications": ["MTC", "MEN2"]
            },
            "mounjaro": {
                "indications": ["Type 2 Diabetes Mellitus"],
                "standard_dose": "2.5 mg once weekly",
                "max_dose": "15 mg once weekly",
                "warnings": ["Severe GI issues"],
                "contraindications": ["MTC"]
            },
            "humalog": {
                "indications": ["Type 1 Diabetes", "Type 2 Diabetes"],
                "standard_dose": "Individualized",
                "max_dose": "Individualized",
                "warnings": ["Hypoglycemia"],
                "contraindications": ["Hypoglycemia"]
            },
            "ozempic": {
                "indications": ["Type 2 Diabetes Mellitus"],
                "standard_dose": "0.25 mg once weekly",
                "max_dose": "2.0 mg once weekly",
                "warnings": ["Pancreatitis", "Gallbladder disease"],
                "contraindications": ["MTC", "MEN2"]
            }
        }
    
    def process(self, state: CaseState) -> CaseState:
        start_time = datetime.now()
        drug = state.order.drug.lower()
        
        data = self.drug_data.get(drug, self.drug_data["trulicity"])
        
        state.drug_info = DrugInfo(
            drug_name=drug,
            indications=data["indications"],
            standard_dose=data["standard_dose"],
            max_dose=data["max_dose"],
            warnings=data["warnings"],
            contraindications=data["contraindications"]
        )
        
        state.status = "drug_retrieved"
        
        latency = (datetime.now() - start_time).total_seconds() * 1000
        
        state.add_audit(
            self.name,
            "drug_info_retrieved",
            {"drug": drug, "found": True, "latency_ms": latency}
        )
        
        return state