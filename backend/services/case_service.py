import pandas as pd
import os
from typing import List, Dict, Any

class CaseService:
    def __init__(self, csv_path: str = "data/cases.csv"):
        self.csv_path = csv_path

    def get_all_cases(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.csv_path):
            return []
        df = pd.read_csv(self.csv_path)
        return df.to_dict(orient="records")

    def get_case_by_id(self, case_id: str) -> Dict[str, Any]:
        cases = self.get_all_cases()
        for case in cases:
            if case["case_id"] == case_id:
                return case
        return None