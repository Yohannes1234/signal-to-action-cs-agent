"""
Mock account data generator for the Signal-to-Action CS Agent.

Generates a set of realistic fake B2B SaaS customer accounts, each with
the four signals defined in design/agent-logic.md:
- usage_trend_pct: % change in product usage over last 30 days (negative = decline)
- unresolved_tickets: number of currently open support tickets
- has_critical_unresolved: whether a critical ticket has been open >7 days
- nps: most recent NPS score (0-10)
- days_since_last_interaction: days since last meaningful customer touchpoint

Run with: python generate_mock_data.py
Output: app/data/mock_accounts.json
"""

import json
import random

COMPANY_NAMES = [
    "Acme Corp", "Northstar", "BrightPath", "Summit Solutions", "Riverside Health",
    "Vertex Inc", "Beacon Labs", "Cobalt Systems", "Lighthouse Analytics", "Pinecrest Group",
    "Meridian Software", "Anchor Digital", "Fieldstone Partners", "Harborview Tech",
    "Ironwood Consulting", "Silverline Data", "Crestview Logistics", "Bluepeak Media",
    "Granite Retail", "Willowbrook Finance", "Cedarline Manufacturing", "Foxglove Studio",
    "Timberline Insurance", "Amberwood Legal", "Clearwater Education",
]

INDUSTRIES = ["Technology", "Healthcare", "Finance", "Education", "Retail", "Manufacturing"]


def generate_account(name: str) -> dict:
    """Generate one realistic account with correlated, plausible signal values."""

    # Pick an overall "health tier" first, then generate signals that plausibly
    # fit that tier — this avoids random noise producing unrealistic combinations
    # (e.g. a happy customer with 6 unresolved critical tickets).
    tier = random.choices(
        ["healthy", "mixed", "at_risk"],
        weights=[0.4, 0.35, 0.25],
    )[0]

    if tier == "healthy":
        usage_trend_pct = round(random.uniform(-8, 20), 1)
        unresolved_tickets = random.randint(0, 1)
        has_critical_unresolved = False
        nps = random.randint(8, 10)
        days_since_last_interaction = random.randint(0, 14)
    elif tier == "mixed":
        usage_trend_pct = round(random.uniform(-30, -5), 1)
        unresolved_tickets = random.randint(1, 3)
        has_critical_unresolved = random.random() < 0.15
        nps = random.randint(5, 8)
        days_since_last_interaction = random.randint(10, 30)
    else:  # at_risk
        usage_trend_pct = round(random.uniform(-65, -25), 1)
        unresolved_tickets = random.randint(2, 6)
        has_critical_unresolved = random.random() < 0.5
        nps = random.randint(0, 6)
        days_since_last_interaction = random.randint(18, 50)

    return {
        "account_id": name.lower().replace(" ", "-"),
        "account_name": name,
        "industry": random.choice(INDUSTRIES),
        "employees": random.choice(["1-50", "51-200", "201-500", "501-1000", "1000+"]),
        "signals": {
            "usage_trend_pct": usage_trend_pct,
            "unresolved_tickets": unresolved_tickets,
            "has_critical_unresolved": has_critical_unresolved,
            "nps": nps,
            "days_since_last_interaction": days_since_last_interaction,
        },
    }


def main():
    random.seed(42)  # fixed seed so results are reproducible for testing/demoing
    accounts = [generate_account(name) for name in COMPANY_NAMES]

    output_path = "app/data/mock_accounts.json"
    with open(output_path, "w") as f:
        json.dump(accounts, f, indent=2)

    print(f"Generated {len(accounts)} mock accounts -> {output_path}")


if __name__ == "__main__":
    main()
