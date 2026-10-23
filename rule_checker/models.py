from pydantic import BaseModel
from typing import Optional

class CheckResult(BaseModel):
    check_name: str
    status: str
    severity: str
    evidence: str
    explanation: str
    recommended_action: Optional[str] = None