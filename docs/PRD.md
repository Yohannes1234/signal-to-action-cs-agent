# Product Requirements Document
## Signal-to-Action: Customer Success Agent

---

## Problem Statement

Customer Success Managers overseeing 80-150 accounts often receive early warning signals — a usage drop, a spike in support tickets, a falling NPS score — but no current platform explains why an account is at risk or what to do next. CSMs must manually piece the story together across multiple tools before they can respond, which delays personalized outreach to accounts that may already be considering leaving.

---

## Persona

Our primary user is a Customer Success Manager at a small to mid-sized B2B SaaS company with a lean CS team — typically managing 80-150 accounts with little dedicated admin or CS Ops support. Their day includes monitoring account health, reviewing engagement and usage data, handling customer issues, preparing for renewals and meetings, and flagging accounts at risk of churn. They rely on several disconnected tools — CRM, CS platform, support desk, email, product-usage dashboards — to piece together a full picture of any one account.

---

## Jobs to Be Done

1. When I receive an alert that a customer may be at risk, I want to quickly understand what changed and what is causing the risk, so I can respond before the issue leads to churn.
2. When several customer accounts show warning signs at the same time, I want to know which accounts need my attention first, so I can focus my limited time on the customers where intervention will have the greatest impact.
3. When I understand why a customer is at risk, I want to quickly prepare relevant and personalized outreach based on that customer's situation, so I can take action without spending additional time gathering information and writing the message from scratch.

---

## Goals

1. **Identify account-level churn risk.** Analyze mocked customer signals such as product usage, support activity, NPS, and engagement using a transparent rule-based scoring system to determine the risk level of an individual account.
2. **Explain why an account is at risk.** Present the key signals contributing to the risk score in clear language so the CSM can quickly understand what changed without manually reviewing multiple data points.
3. **Recommend a next best action.** Based on the identified risk factors, suggest an appropriate action the CSM can take, such as checking in with the customer, addressing a support issue, or discussing declining product adoption.
4. **Generate personalized outreach with human approval.** Draft customer outreach based on the account's risk context while requiring the CSM to review, edit, and approve the message. V1 will not automatically contact customers.

---

## Non-Goals

1. **No autonomous customer communication.** V1 will not automatically send emails or take actions on behalf of the CSM. Human-in-the-loop approval is required to maintain CSM control and reduce the risk of inappropriate AI-generated communication.
2. **No machine-learning churn prediction.** V1 will use transparent, predefined rules to calculate account risk rather than training an ML prediction model. This keeps the initial system explainable and allows the product concept to be validated before introducing model complexity.
3. **No live CRM or third-party integrations.** V1 will use mocked account data rather than connecting directly to Salesforce, HubSpot, Gainsight, ChurnZero, support platforms, or product-analytics systems. Live integrations would add implementation and data-access complexity that is unnecessary for validating the core experience.
4. **No portfolio-wide account ranking.** V1 will evaluate risk at the individual account level and will not rank a CSM's entire portfolio by priority. Portfolio prioritization can be considered later after validating that the account-level risk explanation and recommended actions are useful.

---

## Success Metrics

| Metric | Type | Target | What it validates | Goal |
|---|---|---|---|---|
| Risk explanation comprehension | Leading (measured in testing) | ≥80% of test users correctly identify the primary risk driver | The explanation makes the risk understandable | Goal 2 |
| Next-best-action relevance | Leading (measured in testing) | ≥75% rated relevant/appropriate | Recommendations are useful, not merely generated | Goal 3 |
| Outreach draft acceptance | Leading (measured in testing) | ≥70% require no or only minor edits | AI reduces the effort needed to prepare outreach | Goal 4 |
| Time-to-first-outreach | Lagging (hypothesized, not measured in v1) | Reduction vs. existing workflow | CSMs can move from risk signal to action faster | Goals 2-4 |
| At-risk account retention | Lagging (hypothesized, not measured in v1) | Improvement vs. baseline | Earlier/better intervention ultimately affects retention | Long-term outcome |
