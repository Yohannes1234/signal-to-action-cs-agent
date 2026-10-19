import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchAccountDetail, fetchDraft, logDecision } from "./api";

function DraftReview() {
  const { accountId } = useParams();
  const [account, setAccount] = useState(null);
  const [draft, setDraft] = useState(null);
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [originalSubject, setOriginalSubject] = useState("");
  const [originalBody, setOriginalBody] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [attempt, setAttempt] = useState(0);
  const [decision, setDecision] = useState(null); // null | "approved" | "rejected"
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setLoading(true);
    setError(null);
    Promise.all([fetchAccountDetail(accountId), fetchDraft(accountId)])
      .then(([acct, d]) => {
        setAccount(acct);
        setDraft(d);
        setSubject(d.draft_email.subject);
        setBody(d.draft_email.body);
        setOriginalSubject(d.draft_email.subject);
        setOriginalBody(d.draft_email.body);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [accountId, attempt]);

  const edited = subject !== originalSubject || body !== originalBody;

  function handleDecision(choice) {
    setSaving(true);
    setError(null);
    logDecision(accountId, { decision: choice, edited, subject, body })
      .then(() => setDecision(choice))
      .catch((err) => setError(err.message))
      .finally(() => setSaving(false));
  }

  if (loading) return <p>Generating draft...</p>;

  if (!draft) {
    return (
      <div>
        <Link to={`/accounts/${accountId}`}>&larr; Back to account</Link>
        <div className="error">{error}</div>
        <button onClick={() => setAttempt((a) => a + 1)}>Try again</button>
      </div>
    );
  }

  if (decision) {
    return (
      <div>
        <h1>{decision === "approved" ? "Draft approved" : "Draft rejected"}</h1>
        <div className="card">
          {decision === "approved" ? (
            <p>
              Your decision for {account.account_name} has been recorded
              {edited ? " (with your edits)" : ""}. Nothing was sent. In this
              prototype, approval does not email anyone.
            </p>
          ) : (
            <p>
              The draft for {account.account_name} was rejected and nothing was
              sent.
            </p>
          )}
        </div>
        <Link to="/">&larr; Back to accounts</Link>
      </div>
    );
  }

  return (
    <div>
      <Link to={`/accounts/${accountId}`}>&larr; Back to account</Link>
      <h1>Review draft: {account.account_name}</h1>
      <p>
        <strong>Recommended action:</strong> {draft.recommended_action}
      </p>

      <div className="notice">Nothing will be sent without your approval.</div>

      <div className="card">
        <label>
          <strong>Subject</strong>
          <input
            type="text"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
          />
        </label>

        <div style={{ marginTop: "16px" }}>
          <label>
            <strong>Body</strong>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              rows={16}
            />
          </label>
        </div>
      </div>

      {edited && <p className="meta">You have edited this draft.</p>}
      {error && <div className="error">{error}</div>}

      <div className="actions">
        <button onClick={() => handleDecision("approved")} disabled={saving}>
          Approve
        </button>
        <button
          className="btn-secondary"
          onClick={() => handleDecision("rejected")}
          disabled={saving}
        >
          Reject
        </button>
      </div>
    </div>
  );
}

export default DraftReview;