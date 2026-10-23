import os
import json
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="NetSage AI Backend Engine",
    description="Evidence-backed network troubleshooting with mandatory human review.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REVIEW_LOG_PATH = os.path.join(DATA_DIR, "review_log.json")

# Define /api/review FIRST so it intercepts review requests
@app.post("/api/review")
@app.post("/review")
async def save_review(request: Request):
    try:
        data = await request.json()
        os.makedirs(DATA_DIR, exist_ok=True)

        reviews = []
        if os.path.exists(REVIEW_LOG_PATH):
            with open(REVIEW_LOG_PATH, "r", encoding="utf-8") as f:
                try:
                    reviews = json.load(f)
                except json.JSONDecodeError:
                    reviews = []

        log_entry = {
            "case_id": data.get("case_id", "UNKNOWN"),
            "decision": data.get("decision", "ACCEPTED"),
            "notes": data.get("notes", "User action logged via dashboard"),
            "timestamp": datetime.now().isoformat()
        }
        reviews.append(log_entry)

        with open(REVIEW_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(reviews, f, indent=2)

        print(f"\n[SUCCESS] Saved review for {log_entry['case_id']} to review_log.json\n")
        return {"status": "success", "logged": log_entry}

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Import and mount other routes after /api/review override
from backend.api.routes import router
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "Online", "human_review_required": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)