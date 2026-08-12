# Signal-to-Action: Customer Success Agent
## Project Plan

**What this is:** An agent that detects customer churn-risk signals, reasons about why an account is at risk, and drafts the next best action for a CSM to review and send — closing the gap between "here's a risk score" and "here's what to actually do about it."

**Why human-in-the-loop, not fully autonomous:** Most CS platforms already surface risk scores and alerts. The unsolved problem is the last mile — deciding what to do and writing the outreach. This agent handles that last mile, but a human approves before anything goes out. That's a deliberate scope decision, not a limitation: judgment calls about a customer relationship should stay with a person.

---

## Phase 0 — Setup

- [ ] GitHub repo created
- [ ] Project board set up (Backlog / Discovery / Design / Build / Test / Done)
- [ ] Anthropic API key + billing configured
- [ ] Stack decided, repo scaffolded, `.env` + `.gitignore` in place

**Definition of Done:** repo exists with roadmap and board visible; a secret can't accidentally be committed; a new contributor could clone the repo and know what stack to expect.

---

## Phase 1 — Discovery & Definition (Days 1-3)

### Day 1 — Pain point research
- Read 20-30 real user reviews of Gainsight, ChurnZero, Custify, Vitally, Totango (G2, Capterra, Reddit r/CustomerSuccess, LinkedIn CS groups)
- Tag every complaint into categories (e.g. "too many alerts, no clear action," "manual outreach drafting," "reactive not proactive," "data scattered")
- Rank by frequency

**Output:** `research/pain-points.md` — table of pains, source, frequency, interpretation

### Day 2 — Competitive teardown
- Pick 3 competitors (Gainsight, ChurnZero, Custify)
- For each: what does the AI actually do — score, alert, dashboard, or does it *act*? Pricing tier? Built for enterprise or SMB?
- State the gap explicitly

**Output:** `research/competitive-analysis.md`

### Day 3 — Problem, persona, success metrics
- Problem statement (one sentence: user + pain + why it matters now)
- Target persona (e.g. CSM at a 50-200 person B2B SaaS company managing 80-150 accounts)
- Jobs to be done
- Goals / non-goals — explicit about what v1 will NOT do
- Success metrics: leading (e.g. % of drafted actions approved with no/minor edits) and lagging (e.g. reduction in time-to-outreach)

**Output:** `PRD.md`

**Definition of Done:** the problem statement is backed by ≥15 cited data points from real reviews/discussions, not assumption; the competitive gap is stated in one sentence a stranger could repeat back accurately; non-goals are explicit, not implied.

---

## Phase 2 — Agent Design (Days 4-5)

### Day 4 — Signal & scoring design
- Define signals feeding risk: usage trend, support ticket volume/sentiment, days since last meeting, NPS
- Combine into a score — rule-based (weighted points), not ML, so it's explainable
- Map score bands to next-best-action (e.g. high risk + champion silent → escalate + draft EBR request; medium risk + usage dip only → send check-in)

**Output:** `design/agent-logic.md` — scoring rubric + decision table

### Day 5 — UX flow
- Sketch 3 screens: account list with risk scores, account detail with reasoning, draft review with Approve/Edit/Reject

**Output:** `design/wireframes/`

**Definition of Done:** every score band maps to exactly one named action, with no ambiguous cases left undefined; a reviewer could trace any example account through the rubric by hand and get the same score the system would.

---

## Phase 3 — Build (Days 6-10)

- **Day 6:** Scaffold repo, write mock data generator (20-30 fake accounts: usage trends, tickets, NPS, last-contact date)
- **Day 7:** Build scoring engine — outputs a number and a reasoning string ("Usage down 34% in 30 days + 2 unresolved tickets")
- **Day 8:** Build next-best-action + draft generator via Claude API — prompt engineering until drafts are specific and usable, not generic
- **Day 9:** Build the 3 UI screens, wire to backend/data
- **Day 10:** End-to-end pass, fix rough edges, basic error handling

**Output:** working prototype, deployed or runnable locally with clear setup instructions

**Definition of Done:** a stranger can clone the repo, follow the setup instructions with no help, and get the full flow (account list → reasoning → draft → approve) working end to end.

---

## Phase 4 — Validate (Days 11-12)

- **Day 11:** 3-5 people test it. Structured feedback: Was the reasoning clear? Would you send the draft as-is? Edited? Rejected? Time saved estimate?
- **Day 12:** Synthesize into numbers. Ship one concrete improvement based on feedback.

**Output:** `research/user-feedback.md` — quantified results

**Definition of Done:** at least one success metric from the PRD has a real, cited number attached to it — not an estimate you made up; at least one piece of feedback changed something in the product.

---

## Phase 5 — Finalize (Days 13-14)

- **Day 13:** Write final README: problem → approach & key decisions → demo (GIF/video) → results → what's next
- **Day 14:** Clean up repo structure, add LICENSE, final polish, publish

**Definition of Done:** someone with zero context can read the README top to bottom and understand the problem, the decision, the result, and how to run it — without needing to open any other file.

---

## Working notes
Track day-to-day decisions and open questions in `NOTES.md` as you go — useful for writing the final README later, and for remembering *why* you made a call three weeks from now.
