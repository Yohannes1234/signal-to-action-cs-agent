import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchAccountDetail, fetchDraft } from "./api";

function AccountDetail() {
  const { accountId } = useParams();
  const [account, setAccount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [draft, setDraft] = useState(null);
  const [draftLoading, setDraftLoading] = useState(false);
  const [draftError, setDraftError] = useState(null);

  useEffect(() => {
    fetchAccountDetail(accountId)
      .then(setAccount)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [accountId]);

  function handleGenerate() {
    setDraftLoading(true);
    setDraftError(null);
    fetchDraft(accountId)
      .then(setDraft)
      .catch((err) => setDraftError(err.message))
      .finally(() => setDraftLoading(false));
  }

  if (loading) return <p>Loading account...</p>;
  if (error) return <p>Error: {error}</p>;

  const { signals, signal_levels } = account;
  const isLow = account.risk_band === "low";

  return (
    <div>
      <Link to="/">&larr; Back to accounts</Link>
      <h1>{account.account_name}</h1>
      <p>
        {account.industry} · {account.employees} employees
      </p>

      <p>
        <strong>Risk band:</strong> {account.risk_band} (score{" "}
        {account.base_score}/8)
        {account.override_fired && " — escalation override applied"}
      </p>
      <p>
        <strong>Primary driver:</strong> {account.primary_driver}
      </p>

      <h2>Signals</h2>
      <table>
        <thead>
          <tr>
            <th>Signal</th>
            <th>Value</th>
            <th>Level</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Usage trend</td>
            <td>{signals.usage_trend_pct}%</td>
            <td>{signal_levels.usage_trend}</td>
          </tr>
          <tr>
            <td>Support activity</td>
            <td>
              {signals.unresolved_tickets} unresolved{" "}
              {signals.unresolved_tickets === 1 ? "ticket" : "tickets"}
            </td>
            <td>{signal_levels.support_activity}</td>
          </tr>
          <tr>
            <td>NPS</td>
            <td>{signals.nps}</td>
            <td>{signal_levels.nps}</td>
          </tr>
          <tr>
            <td>Engagement recency</td>
            <td>{signals.days_since_last_interaction} days since last contact</td>
            <td>{signal_levels.engagement_recency}</td>
          </tr>
        </tbody>
      </table>

      <h2>{isLow ? "Account summary" : "Why this account is at risk"}</h2>
      {!draft && (
        <button onClick={handleGenerate} disabled={draftLoading}>
          {draftLoading
            ? "Generating..."
            : isLow
            ? "Summarize account"
            : "Explain risk & recommend action"}
        </button>
      )}
      {draftError && <p>Error: {draftError}</p>}
      {draft && (
        <div>
          <p>{draft.explanation}</p>
          <p>
            <strong>Recommended action:</strong> {draft.recommended_action}
          </p>
        </div>
      )}
    </div>
  );
}

export default AccountDetail;