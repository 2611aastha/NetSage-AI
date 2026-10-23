from pydantic import BaseModel
from typing import List, Optional

class CaseSchema(BaseModel):
    case_id: str
    symptom: str
    topology_note: str
    show_outputs: str
    expected_fault: str
    osi_layer: str
    concept: str
    severity: str

class AiDiagnosisResponse(BaseModel):
    root_cause: str
    confidence: int
    confidence_level: str
    evidence: List[str]
    next_command: str
    fix_steps: List[str]
    osi_layer: str
    concept: str
    alternative_hypotheses: List[str]
    human_review_required: bool = True

class ReviewSubmission(BaseModel):
    case_id: str
    reviewer: str
    decision: str
    correction_notes: Optional[str] = ""
    updated_fix: Optional[str] = None