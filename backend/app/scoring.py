def score_usage_trend(usage_trend_pct: float) -> str:
    """
    Returns 'low', 'medium', or 'high' based on usage_trend_pct
    (negative = decline). Rules from agent-logic.md section 1.
    """
    if usage_trend_pct > -10:
        return "low"
    elif usage_trend_pct > -30:
        return "medium"
    else:
        return "high"


def score_support_activity(unresolved_tickets: int, has_critical_unresolved: bool = False) -> str:
    """
    Returns 'low', 'medium', or 'high'.
    Rules: 0-1 unresolved -> low. 2-3 unresolved -> medium.
    4+ unresolved, OR a critical ticket unresolved >7 days -> high.
    """
    if has_critical_unresolved or unresolved_tickets >= 4:
        return "high"
    elif unresolved_tickets >= 2:
        return "medium"
    else:
        return "low"


def score_nps(nps: int) -> str:
    """
    Returns 'low', 'medium', or 'high'.
    Rules: NPS 9-10 -> low. NPS 7-8 -> medium. NPS 0-6 -> high.
    """
    if nps >= 9:
        return "low"
    elif nps >= 7:
        return "medium"
    else:
        return "high"


def score_engagement_recency(days_since_last_interaction: int) -> str:
    """
    Returns 'low', 'medium', or 'high'.
    Rules: <=14 days -> low. 15-30 days -> medium. >30 days -> high.
    """
    if days_since_last_interaction <= 14:
        return "low"
    elif days_since_last_interaction <= 30:
        return "medium"
    else:
        return "high"


def calculate_base_score(signal_levels: dict) -> int:
    """
    Takes a dict of signal_name -> risk_level ('low'/'medium'/'high')
    and returns the total base score (0-8).
    """
    points_map = {"low": 0, "medium": 1, "high": 2}
    return sum(points_map[level] for level in signal_levels.values())


def score_to_risk_band(base_score: int) -> str:
    """
    Converts the total base score (0-8) into a risk band.
    Rules: 0-2 -> low, 3-5 -> medium, 6-8 -> high.
    """
    if base_score <= 2:
        return "low"
    elif base_score <= 5:
        return "medium"
    else:
        return "high"

def check_escalation_override(account_signals: dict) -> bool:
    """
    Returns True if any escalation override condition is met,
    forcing the account to High risk regardless of base score.
    Rules from agent-logic.md section 3.
    """
    critical_ticket = account_signals["has_critical_unresolved"]
    severe_usage_decline = account_signals["usage_trend_pct"] < -50
    hard_detractor = account_signals["nps"] <= 3

    return critical_ticket or severe_usage_decline or hard_detractor

def determine_primary_driver(signal_levels: dict) -> str:
    """
    Determines which signal is the primary driver of risk, using the
    priority order Support > Sentiment > Usage > Engagement to break
    ties among signals at the same (highest) severity.
    Rules from agent-logic.md section 4.
    """
    priority_order = ["support_activity", "nps", "usage_trend", "engagement_recency"]
    severity_rank = {"low": 0, "medium": 1, "high": 2}

    highest_severity = max(severity_rank[level] for level in signal_levels.values())

    for signal_name in priority_order:
        if severity_rank[signal_levels[signal_name]] == highest_severity:
            return signal_name


def score_account(account_signals: dict) -> dict:
    """
    Takes an account's raw signals and returns the complete risk
    assessment: individual signal levels, base score, risk band,
    whether an override fired, and the primary driver.
    """
    signal_levels = {
        "usage_trend": score_usage_trend(account_signals["usage_trend_pct"]),
        "support_activity": score_support_activity(
            account_signals["unresolved_tickets"],
            account_signals["has_critical_unresolved"],
        ),
        "nps": score_nps(account_signals["nps"]),
        "engagement_recency": score_engagement_recency(
            account_signals["days_since_last_interaction"]
        ),
    }

    base_score = calculate_base_score(signal_levels)
    override_fired = check_escalation_override(account_signals)

    if override_fired:
        risk_band = "high"
    else:
        risk_band = score_to_risk_band(base_score)

    primary_driver = determine_primary_driver(signal_levels)

    return {
        "signal_levels": signal_levels,
        "base_score": base_score,
        "override_fired": override_fired,
        "risk_band": risk_band,
        "primary_driver": primary_driver,
    }



if __name__ == "__main__":
    acme_signals = {
        "usage_trend_pct": -42,
        "unresolved_tickets": 3,
        "has_critical_unresolved": False,
        "nps": 5,
        "days_since_last_interaction": 21,
    }
    result = score_account(acme_signals)
    print(result)