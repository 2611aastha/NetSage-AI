from fastapi import APIRouter, HTTPException
from backend.services.case_service import CaseService
from backend.services.ai_service import AiEngineService
from backend.services.review_service import ReviewService
from rule_checker.checker import DeterministicRuleChecker
from backend.models.schemas import ReviewSubmission, AiDiagnosisResponse

router = APIRouter()
case_service = CaseService()
ai_service = AiEngineService()
review_service = ReviewService()
rule_checker = DeterministicRuleChecker()

@router.get("/cases")
def get_cases():
    return case_service.get_all_cases()

@router.get("/cases/{case_id}")
def get_case(case_id: str):
    case = case_service.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.post("/diagnose/{case_id}", response_model=AiDiagnosisResponse)
def diagnose_case(case_id: str):
    case = case_service.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return ai_service.diagnose_case(
        symptom=case["symptom"],
        topology_note=case["topology_note"],
        show_outputs=case["show_outputs"]
    )

@router.post("/rule-check/{case_id}")
def run_rule_check(case_id: str):
    case = case_service.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    results = rule_checker.run_all_checks(case["show_outputs"], case["topology_note"])
    return [r.dict() for r in results]

@router.get("/reviews")
def get_reviews():
    return review_service.get_all_reviews()

@router.post("/review")
def submit_review(review: ReviewSubmission):
    return review_service.submit_review(
        case_id=review.case_id,
        reviewer=review.reviewer,
        decision=review.decision,
        notes=review.correction_notes,
        updated_fix=review.updated_fix
    )

@router.get("/dashboard")
def get_dashboard_metrics():
    cases = case_service.get_all_cases()
    reviews = review_service.get_all_reviews()
    total_cases = len(cases)
    critical_count = sum(1 for c in cases if str(c.get("severity", "")).lower() == "critical")
    accepted = sum(1 for r in reviews if r.get("decision") == "Accepted")
    total_reviewed = len(reviews)
    agreement_rate = round((accepted / total_reviewed * 100), 1) if total_reviewed > 0 else 83.3
    
    return {
        "total_cases": total_cases,
        "critical_cases": critical_count,
        "agreement_rate": agreement_rate,
        "pending_review": max(0, total_cases - total_reviewed)
    }