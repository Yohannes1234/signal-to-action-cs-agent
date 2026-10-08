## Scope decision: tabs and template dropdown are placeholders in v1

Signals, History, and Notes tabs, and the "Use template" dropdown, are
visual placeholders in the Figma prototype — not functional in v1.
V1 build is scoped strictly to: account-level risk identification →
risk explanation → recommended next action → editable outreach draft →
human approval. Validating this core workflow first; expanded tabs
and template functionality are a candidate for a later iteration.

## Bug found in testing: AI explanation contradicted the data

**What happened:** For a healthy account (score 0/8, NPS 10, all signals low), the AI explanation said the NPS of 10 "indicates significant dissatisfaction" and that the account might be "quietly disengaging."

**Root cause:**
- The prompt never told Claude the overall risk band or the NPS scale, so it read "low" as a bad value instead of low risk.
- The scoring logic's tie-break still picked a primary driver (support_activity) when every signal was low, and the prompt asked Claude to explain why that driver was a risk.

**Fix:**
- Passed the risk band and scale definitions into the prompt, plus an explicit rule for low-risk accounts (summarize as healthy, no rescue email).
- Raised `max_tokens` from 500 to 1000 so longer responses can't be cut off mid-JSON.
- Verified on one low-risk account (Clearwater) and one high-risk account (Lighthouse): the low-risk explanation is now consistent with the data, and the high-risk case still leads with the primary driver.

## Follow-up fix: primary driver only for Medium/High risk

**What happened:** Cedarline (score 1/8, healthy) still showed NPS as its "primary driver," because NPS was the only signal above low.

**Fix:** `score_account` now returns a primary driver of "none" when the risk band is low. A driver is only assigned for Medium/High accounts, including those forced to High by an escalation override. The detail screen shows "None (no elevated risk)" and the heading and button adapt to the band.

**Lesson:** my first rule ("no signal above low means no driver") was too narrow. Tying the driver to the risk band is the correct condition.

## Doc/code alignment

Updated `design/agent-logic.md` to match the implemented rules:
- Usage threshold boundary (exactly -30% is High).
- The NPS escalation override fires on NPS 0-3 alone, since v1 has no feedback text.
- Removed the "Medium risk, no dominant driver" action row, which the code never produces.
- Marked qualitative conditions (rising ticket volume, text-based sentiment) as future work.