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


if __name__ == "__main__":
    print(score_usage_trend(-42))
    print(score_support_activity(3))
    print(score_nps(5))
    print(score_engagement_recency(21))