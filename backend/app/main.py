import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.scoring import score_account, map_driver_to_action
from app.agent import generate_explanation_and_draft

app = FastAPI(title="Signal-to-Action CS Agent")

# Allows the frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_accounts():
    with open("app/data/mock_accounts.json") as f:
        return json.load(f)


@app.get("/accounts")
def list_accounts():
    """Screen 1: account list with risk band and primary driver."""
    accounts = load_accounts()
    results = []
    for acc in accounts:
        scored = score_account(acc["signals"])
        results.append({
            "account_id": acc["account_id"],
            "account_name": acc["account_name"],
            "industry": acc["industry"],
            "risk_band": scored["risk_band"],
            "primary_driver": scored["primary_driver"],
        })
    return results


@app.get("/accounts/{account_id}")
def get_account_detail(account_id: str):
    """Screen 2: full signal breakdown and reasoning for one account."""
    accounts = load_accounts()
    account = next((a for a in accounts if a["account_id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    scored = score_account(account["signals"])
    return {
        "account_id": account["account_id"],
        "account_name": account["account_name"],
        "industry": account["industry"],
        "employees": account["employees"],
        "signals": account["signals"],
        **scored,
    }


@app.post("/accounts/{account_id}/draft")
def get_draft(account_id: str):
    """Screen 3: generates the recommended action and AI draft outreach."""
    accounts = load_accounts()
    account = next((a for a in accounts if a["account_id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    scored = score_account(account["signals"])
    action = map_driver_to_action(scored["primary_driver"], scored["risk_band"])
    output = generate_explanation_and_draft(
        account["account_name"], account["signals"], scored["signal_levels"],
        scored["primary_driver"], action, scored["risk_band"]
    )
    return {
        "recommended_action": action,
        "explanation": output["explanation"],
        "draft_email": output["draft_email"],
    }


class DecisionIn(BaseModel):
    decision: str   # "approved" or "rejected"
    edited: bool    # did the CSM change the draft before deciding?
    subject: str
    body: str


@app.post("/accounts/{account_id}/decision")
def log_decision(account_id: str, payload: DecisionIn):
    """Records the CSM's approve/reject decision. Nothing is ever sent."""
    if payload.decision not in ("approved", "rejected"):
        raise HTTPException(status_code=400, detail="decision must be 'approved' or 'rejected'")

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "account_id": account_id,
        "decision": payload.decision,
        "edited": payload.edited,
        "subject": payload.subject,
        "body": payload.body,
    }
    log_path = Path(__file__).parent / "data" / "decisions.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    return {"status": "logged"}