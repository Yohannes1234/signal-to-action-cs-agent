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


if __name__ == "__main__":
    print(score_usage_trend(-42))
    print(score_support_activity(3))
    print(score_nps(5))
    print(score_engagement_recency(21))