# Usability Test Script

**Goal:** check whether the three leading metrics in the PRD hold up with real users:
explanation comprehension, next-action relevance, and draft acceptance.

**Participants:** 3-5 people who work in, or close to, customer success or account
management. Each session takes about 15 minutes.

## Before each session
- Backend and frontend are both running.
- `backend/app/data/decisions.jsonl` is deleted (so only real decisions are logged).
- Notes template (`research/user-feedback.md`) is open.

## Intro (read aloud, don't improvise)
"This is a prototype that flags at-risk customer accounts, explains why, and drafts
an outreach email. All the data is fake and nothing is ever sent. I'm testing the
product, not you, so there are no wrong answers. Please think out loud as you go."

## Tasks
1. **Find the account most at risk.** Starting on the list page, find an account you
   think needs attention first. (Observe: what do they click, and why?)
2. **Understand why.** On a high- or medium-risk account, ask for the explanation.
   "In your own words, why is this account at risk?"
3. **Judge the recommendation.** "The tool recommends this action. Would you take it?"
4. **Review the draft.** Open the draft email. "Would you send this? Change anything
   you'd want changed."
5. **Decide.** Ask them to approve or reject it.

## Questions after the tasks (ask exactly as written)
1. Q1: "Did the explanation make clear why the account is at risk?" (Yes / Partly / No)
2. Q2: "Was the recommended action the right one for this account?" (Yes / Partly / No)
3. Q3: "Would you send the draft as written, with minor edits, or not at all?"
   (As is / Minor edits / No)
4. Q4: "What was confusing, missing, or wrong?" (open-ended)
5. Q5: "How long would this normally take you without the tool?" (self-reported estimate)

## Rules
- Don't explain the screens or help them. Write down where they get stuck.
- Record answers as given. Don't reword them afterward.
- Never present these results as proof the product works. See the reporting rules in
  `research/user-feedback.md`.