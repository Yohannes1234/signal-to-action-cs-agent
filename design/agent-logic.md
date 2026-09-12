# Agent Logic: Risk Scoring & Next-Best-Action

This document defines, before any code is written, exactly how account risk is calculated and how a risk profile maps to a recommended action. The goal is a system a CSM can trust because its reasoning is fully traceable — no black box.

---

## 1. Signals

Four signals are evaluated per account. Each is scored independently as Low / Medium / High.

| Signal | Low Risk | Medium Risk | High Risk |
|---|---|---|---|
| **Usage trend** | Stable/growing, or decline <10% in 30 days | Decline of 10-30% | Decline >30% |
| **Support activity** | 0-1 unresolved tickets | 2-3 unresolved tickets, or rising ticket volume | 4+ unresolved tickets, or a critical issue unresolved >7 days |
| **NPS / sentiment** | NPS 9-10, or clearly positive sentiment | NPS 7-8, or neutral/mixed sentiment | NPS 0-6, or clearly negative sentiment |
| **Engagement recency** | Meaningful interaction within 14 days | 15-30 days since last interaction | >30 days since last interaction |

**Design note:** ticket volume alone is not treated as risky — only unresolved and high-severity issues carry weight, since normal support activity is expected and not itself a churn signal.

---

## 2. Base Score

Each signal contributes points based on its risk level: **Low = 0, Medium = 1, High = 2.**

With four signals, the total ranges from 0 to 8.

| Total Score | Overall Risk |
|---|---|
| 0-2 | Low |
| 3-5 | Medium |
| 6-8 | High |

---

## 3. Escalation Overrides

Not all signals are equally consequential. Some conditions are severe enough that they should force an account to High risk regardless of the total score — a strong average across other signals shouldn't be allowed to dilute an active, serious problem.

An account is automatically classified **High risk** if any of the following are true, regardless of total score:

- A critical/high-severity support ticket has been unresolved for more than 7 days
- Usage has declined more than 50% in 30 days
- NPS is 0-3 **and** recent feedback contains explicit dissatisfaction or churn-related language

**Design rationale:** this makes the "not all signals are equal" judgment explicit and auditable, rather than hidden inside a weighting formula that would be harder to explain and defend (e.g. "why is support weighted 2.3x?"). A CSM or reviewer can see exactly which override fired and why.

---

## 4. Determining the Primary Driver

When an account is Medium or High risk, the system identifies the **primary driver** — the signal most responsible for the risk classification — using this priority order when multiple signals are elevated simultaneously:

**Support > Sentiment > Usage > Engagement**

**Rationale for this order:** an active unresolved problem (support) is the most urgent to address, followed by explicit unhappiness (sentiment), then behavioral decline (usage), then mere silence (engagement) — silence alone is the weakest and most ambiguous signal of the four.

If only one signal is elevated, that signal is automatically the primary driver.

**Ties:** if two or more signals are tied at the highest severity, the priority order (Support > Sentiment > Usage > Engagement) breaks the tie — the higher-priority signal wins and becomes the primary driver.

### Primary driver vs. supporting signals

**The primary driver determines the recommended action. All elevated signals — primary and supporting — inform the generated explanation and the drafted outreach.**

This keeps the system deterministic and traceable (one clear rule decides *what to recommend*) while still producing outreach that reads as genuinely aware of the account's full context, not a single-signal template. An engineer or reviewer should always be able to look at the signal table, apply the priority order, and predict which action fires — the language of the explanation and draft is the only part that draws on the supporting signals.

---

## 5. Risk → Action Mapping

| Primary Driver | Recommended Action |
|---|---|
| Support (critical/unresolved) | Escalate internally; CSM outreach offering direct resolution |
| Sentiment (negative NPS/feedback) | Personal CSM outreach addressing the specific dissatisfaction |
| Usage (declining) | Schedule a business review or re-engagement call; investigate adoption barriers |
| Engagement (silence only) | Lightweight check-in email |
| Medium risk, no dominant driver | Proactive check-in; continue monitoring |
| Low risk | No action; routine monitoring |

---

## 6. Worked Example

**Account: Acme Corp**
- Usage trend: declined 42% in 30 days → **High (2 pt)**
- Support activity: 3 unresolved tickets, none critical → **Medium (1 pt)**
- NPS/sentiment: NPS 5 (detractor) → **High (2 pt)**
- Engagement recency: last interaction 21 days ago → **Medium (1 pt)**

**Base score:** 2 + 1 + 2 + 1 = 6 → **High risk**
**Escalation override check:** none triggered (no single override condition met)
**Primary driver:** Usage and Sentiment are tied at High — the priority order (Support > Sentiment > Usage > Engagement) breaks the tie in favor of **Sentiment**
**Recommended action:** Reach out to understand and address customer dissatisfaction (driven by the Sentiment mapping in Section 5)
**Explanation/draft generation:** incorporates all elevated signals — sentiment (primary), plus usage decline, unresolved tickets, and reduced engagement (supporting) — producing a message that references the fuller picture, not just the primary driver alone

This example should be traceable by hand — anyone reading this document can recompute the same result the system would produce, including which signal wins the tie-break and why.

---

## 7. Explicit Boundaries (see PRD Non-Goals)

- Scoring is rule-based and fixed, not learned or adjusted by machine learning (Non-Goal 2)
- Signals use mocked data, not live integrations (Non-Goal 3)
- This logic scores individual accounts only; it does not rank a CSM's full portfolio (Non-Goal 4)
