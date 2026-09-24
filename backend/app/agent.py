import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()  # automatically reads ANTHROPIC_API_KEY from the environment



def generate_explanation_and_draft(account_name: str, signals: dict, signal_levels: dict,
                                     primary_driver: str, recommended_action: str) -> dict:
    """
    Calls Claude to generate a plain-language risk explanation and a
    personalized outreach draft, based on the deterministic scoring
    and action-mapping results (never on its own judgment of risk).
    """

    prompt = f"""You are helping a Customer Success Manager understand why an account is at risk and prepare outreach.

Account: {account_name}
Signals:
- Usage trend: {signals['usage_trend_pct']}% change in 30 days ({signal_levels['usage_trend']})
- Support activity: {signals['unresolved_tickets']} unresolved tickets, critical unresolved: {signals['has_critical_unresolved']} ({signal_levels['support_activity']})
- NPS: {signals['nps']} ({signal_levels['nps']})
- Engagement: {signals['days_since_last_interaction']} days since last interaction ({signal_levels['engagement_recency']})

The primary driver of risk is: {primary_driver}
The recommended action is: {recommended_action}

Respond with ONLY valid JSON, no markdown formatting, no code fences, no other text — just the raw JSON object, in this exact format:
{{
  "explanation": "2-3 sentence plain-language explanation of why this account is at risk, referencing the primary driver first and supporting signals second",
  "draft_email": {{
    "subject": "short email subject line",
    "body": "email body text, addressing the primary driver and naturally referencing supporting signals"
  }}
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
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
        result["primary_driver"], action
    )
    print(output["explanation"])
    print("---")
    print("Subject:", output["draft_email"]["subject"])
    print(output["draft_email"]["body"])