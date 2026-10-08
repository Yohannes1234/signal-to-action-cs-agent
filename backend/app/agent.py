import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()  # automatically reads ANTHROPIC_API_KEY from the environment


def generate_explanation_and_draft(account_name: str, signals: dict, signal_levels: dict,
                                     primary_driver: str, recommended_action: str,
                                     risk_band: str) -> dict:
    """
    Calls Claude to generate a plain-language risk explanation and a
    personalized outreach draft, based on the deterministic scoring
    and action-mapping results (never on its own judgment of risk).
    """

    prompt = f"""You are helping a Customer Success Manager understand an account's health and prepare outreach.

IMPORTANT: The risk assessment below was computed by a deterministic scoring system. Do not re-judge it, contradict it, or invent causes that are not in the data. Only explain and phrase what the data shows.

How to read the data:
- Each signal level (low/medium/high) is a RISK level, not a quality level. "low" means little risk (healthy); "high" means high risk.
- NPS is on a 0-10 scale: 9-10 is a promoter (very satisfied), 7-8 is passive, 0-6 is a detractor (dissatisfied).
- Usage trend is the % change over 30 days; a negative number is a decline.

Account: {account_name}
Overall risk band: {risk_band}
Signals:
- Usage trend: {signals['usage_trend_pct']}% change in 30 days (risk level: {signal_levels['usage_trend']})
- Support activity: {signals['unresolved_tickets']} unresolved tickets, critical unresolved: {signals['has_critical_unresolved']} (risk level: {signal_levels['support_activity']})
- NPS: {signals['nps']} (risk level: {signal_levels['nps']})
- Engagement: {signals['days_since_last_interaction']} days since last interaction (risk level: {signal_levels['engagement_recency']})

Primary driver: {primary_driver}
Recommended action: {recommended_action}

Rules:
- If the overall risk band is "low", say the account looks healthy. Do not describe risk or concerns, and do not treat the primary driver as a problem. Write a short, positive check-in email (not a rescue email).
- If the band is "medium" or "high", lead with the primary driver, then use supporting signals for context. Only mention a signal as a concern if its risk level is medium or high.
- Never describe a signal in a way that contradicts its value or risk level.
- Never invent facts (history, causes, events) that are not in the data above.

Respond with ONLY valid JSON, no markdown formatting, no code fences, no other text, in this exact format:
{{
  "explanation": "2-3 sentence plain-language summary of the account's situation, consistent with the risk band",
  "draft_email": {{
    "subject": "short email subject line",
    "body": "email body text appropriate to the risk band"
  }}
}}"""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    import json
    raw_text = response.content[0].text.strip()

    # Strip markdown code fences if present (Claude sometimes adds them
    # despite instructions not to)
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    return json.loads(raw_text)

if __name__ == "__main__":
    from scoring import score_account, map_driver_to_action

    acme_signals = {
        "usage_trend_pct": -42,
        "unresolved_tickets": 3,
        "has_critical_unresolved": False,
        "nps": 5,
        "days_since_last_interaction": 21,
    }
    result = score_account(acme_signals)
    action = map_driver_to_action(result["primary_driver"], result["risk_band"])

    output = generate_explanation_and_draft(
        "Acme Corp", acme_signals, result["signal_levels"],
        result["primary_driver"], action, result["risk_band"]
    )
    print(output["explanation"])
    print("---")
    print("Subject:", output["draft_email"]["subject"])
    print(output["draft_email"]["body"])