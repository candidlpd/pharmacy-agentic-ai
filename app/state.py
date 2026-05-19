"""
STATE MANAGEMENT
Defines the shared state that flows through all agents
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class CaseStatus(str, Enum):
    STARTED = "started"
    INTAKE_COMPLETE = "intake_complete"
    DRUG_RETRIEVED = "drug_retrieved"
    COVERAGE_CHECKED = "coverage_checked"
    SAFETY_CHECKED = "safety_checked"
    RISK_ASSESSED = "risk_assessed"
    DECISION_MADE = "decision_made"
    COMPLETED = "completed"
    ERROR = "error"
    HITL_REQUIRED = "hitl_required"


@dataclass
class Patient:
    name: str = ""
    allergies: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    age: int = 0
    
    def to_dict(self) -> Dict:
        return {"name": self.name, "allergies": self.allergies, "conditions": self.conditions, "age": self.age}


@dataclass
class MedicationOrder:
    drug: str = ""
    dose: str = ""
    frequency: str = ""
    indication: str = ""
    
    def to_dict(self) -> Dict:
        return {"drug": self.drug, "dose": self.dose, "indication": self.indication}


@dataclass
class DrugInfo:
    drug_name: str = ""
    indications: List[str] = field(default_factory=list)
    standard_dose: str = ""
    max_dose: str = ""
    warnings: List[str] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "drug_name": self.drug_name,
            "indications": self.indications,
            "standard_dose": self.standard_dose,
            "max_dose": self.max_dose,
            "warnings": self.warnings
        }


@dataclass
class CoverageInfo:
    tier: int = 2
    pa_required: bool = False
    copay: str = "$60"
    
    def to_dict(self) -> Dict:
        return {"tier": self.tier, "pa_required": self.pa_required, "copay": self.copay}


@dataclass
class SafetyInfo:
    dose_ok: bool = True
    allergy_warnings: List[str] = field(default_factory=list)
    safety_flags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {"dose_ok": self.dose_ok, "allergy_warnings": self.allergy_warnings, "safety_flags": self.safety_flags}


@dataclass
class RiskAssessment:
    risk_score: float = 0.0
    risk_level: str = "LOW"
    
    def to_dict(self) -> Dict:
        return {"risk_score": self.risk_score, "risk_level": self.risk_level}


@dataclass
class Decision:
    approved: bool = False
    reason: str = ""
    requires_hitl: bool = False
    
    def to_dict(self) -> Dict:
        return {"approved": self.approved, "reason": self.reason, "requires_hitl": self.requires_hitl}


@dataclass
class CaseState:
    """MAIN STATE - Passed through all agents"""
    
    case_id: str = ""
    patient: Patient = field(default_factory=Patient)
    order: MedicationOrder = field(default_factory=MedicationOrder)
    
    drug_info: DrugInfo = field(default_factory=DrugInfo)
    coverage_info: CoverageInfo = field(default_factory=CoverageInfo)
    safety_info: SafetyInfo = field(default_factory=SafetyInfo)
    risk_assessment: RiskAssessment = field(default_factory=RiskAssessment)
    decision: Decision = field(default_factory=Decision)
    
    status: str = "started"
    audit_trail: List[Dict] = field(default_factory=list)
    
    def add_audit(self, agent: str, action: str, data: Dict = None):
        self.audit_trail.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "action": action,
            "data": data or {}
        })
    
    def to_dict(self) -> Dict:
        return {
            "case_id": self.case_id,
            "patient": self.patient.to_dict(),
            "order": self.order.to_dict(),
            "drug_info": self.drug_info.to_dict(),
            "coverage": self.coverage_info.to_dict(),
            "safety": self.safety_info.to_dict(),
            "risk": self.risk_assessment.to_dict(),
            "decision": self.decision.to_dict(),
            "status": self.status
        }