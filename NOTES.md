
## Scope decision: tabs and template dropdown are placeholders in v1

Signals, History, and Notes tabs, and the "Use template" dropdown, are
visual placeholders in the Figma prototype — not functional in v1.
V1 build is scoped strictly to: account-level risk identification →
risk explanation → recommended next action → editable outreach draft
→ human approval. Validating this core workflow first; expanded tabs
and template functionality are a candidate for a later iteration.

## Bug found in testing: AI explanation contradicted the data

**What happened:** For a healthy account (score 0/8, NPS 10, all signals low), the AI explanation said the NPS of 10 "indicates significant dissatisfaction" and that the account might be "quietly disengaging."

**Root cause:**
- The prompt never told Claude the overall risk band or the NPS scale, so it read "low" as a bad value instead of low risk.
- The scoring logic's tie-break still picked a primary driver (support_activity) when every signal was low, and the prompt asked Claude to explain why that driver was a risk.

**Fix:**
- Pass risk band and scale definitions into the prompt, plus an explicit rule for low-risk accounts.
- Next: return no primary driver when no signal exceeds low.