import json
import os
from datetime import datetime
from typing import List, Dict, Any

class ReviewService:
    def __init__(self, review_log_path: str = "data/review_log.json"):
        self.review_log_path = review_log_path

    def get_all_reviews(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.review_log_path):
            return []
        with open(self.review_log_path, "r") as f:
            return json.load(f)

    def submit_review(self, case_id: str, reviewer: str, decision: str, notes: str, updated_fix: str = None) -> Dict[str, Any]:
        reviews = self.get_all_reviews()
        record = {
            "case_id": case_id,
            "reviewer": reviewer,
            "decision": decision,
            "correction_notes": notes,
            "updated_fix": updated_fix,
            "timestamp": datetime.now().isoformat()
        }
        reviews.append(record)
        with open(self.review_log_path, "w") as f:
            json.dump(reviews, f, indent=2)
        return record