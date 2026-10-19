import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchAccountDetail, fetchDraft } from "./api";
import { driverLabel } from "./labels";

function AccountDetail() {
  const { accountId } = useParams();
  const [account, setAccount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [attempt, setAttempt] = useState(0);

  const [draft, setDraft] = useState(null);
  const [draftLoading, setDraftLoading] = useState(false);
  const [draftError, setDraftError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchAccountDetail(accountId)
      .then(setAccount)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [accountId, attempt]);

  function handleGenerate() {
    setDraftLoading(true);
    setDraftError(null);
    fetchDraft(accountId)
      .then(setDraft)
      .catch((err) => setDraftError(err.message))
      .finally(() => setDraftLoading(false));
  }

  if (loading) return <p>Loading account...</p>;
  if (error) {
    return (
      <div>
        <Link to="/">&larr; Back to accounts</Link>
        <div className="error">{error}</div>
        <button onClick={() => setAttempt((a) => a + 1)}>Try again</button>
      </div>
    );
  }

  const { signals, signal_levels } = account;
  const isLow = account.risk_band === "low";

  return (
    <div>
      <Link to="/">&larr; Back to accounts</Link>
      <h1>{account.account_name}</h1>
      <p className="meta">
        {account.industry} · {account.employees} employees
      </p>

      <div className="card">
        <p>
          <strong>Risk band:</strong>{" "}
          <span className={`badge badge-${account.risk_band}`}>
            {account.risk_band}
          </span>{" "}
          (score {account.base_score}/8)
          {account.override_fired && " — escalation override applied"}
        </p>
        <p>
          <strong>Primary driver:</strong> {driverLabel(account.primary_driver)}
        </p>
      </div>

      <h2>Signals</h2>
      <table>
        <thead>
          <tr>
            <th>Signal</th>
            <th>Value</th>
            <th>Risk level</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Usage trend</td>
            <td>{signals.usage_trend_pct}%</td>
            <td>
              <span className={`badge badge-${signal_levels.usage_trend}`}>
                {signal_levels.usage_trend}
              </span>
            </td>
          </tr>
          <tr>
            <td>Support activity</td>
            <td>
              {signals.unresolved_tickets} unresolved{" "}
              {signals.unresolved_tickets === 1 ? "ticket" : "tickets"}
            </td>
            <td>
              <span className={`badge badge-${signal_levels.support_activity}`}>
                {signal_levels.support_activity}
              </span>
            </td>
          </tr>
          <tr>
            <td>NPS</td>
            <td>{signals.nps}</td>
            <td>
              <span className={`badge badge-${signal_levels.nps}`}>
                {signal_levels.nps}
              </span>
            </td>
          </tr>
          <tr>
            <td>Engagement recency</td>
            <td>{signals.days_since_last_interaction} days since last contact</td>
            <td>
              <span
                className={`badge badge-${signal_levels.engagement_recency}`}
              >
                {signal_levels.engagement_recency}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <h2>{isLow ? "Account summary" : "Why this account is at risk"}</h2>
      {draftError && <div className="error">{draftError}</div>}
      {!draft && (
        <button onClick={handleGenerate} disabled={draftLoading}>
          {draftLoading
            ? "Generating..."
            : draftError
            ? "Try again"
            : isLow
            ? "Summarize account"
            : "Explain risk & recommend action"}
        </button>
      )}
      {draft && (
        <div>
          <div className="card">
            <p>{draft.explanation}</p>
          </div>
          <p>
            <strong>Recommended action:</strong> {draft.recommended_action}
          </p>
          {!isLow && (
            <p>
              <Link to={`/accounts/${accountId}/review`}>
                Review draft outreach &rarr;
              </Link>
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default AccountDetail;