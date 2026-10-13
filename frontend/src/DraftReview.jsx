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
  const [decision, setDecision] = useState(null); // null | "approved" | "rejected"
  const [saving, setSaving] = useState(false);

  useEffect(() => {
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
  }, [accountId]);

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
  if (error && !draft) return <p>Error: {error}</p>;

  if (decision) {
    return (
      <div>
        <h1>{decision === "approved" ? "Draft approved" : "Draft rejected"}</h1>
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

      <p>
        <em>Nothing will be sent without your approval.</em>
      </p>

      <div>
        <label>
          <strong>Subject</strong>
          <br />
          <input
            type="text"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            style={{ width: "100%" }}
          />
        </label>
      </div>

      <div style={{ marginTop: "12px" }}>
        <label>
          <strong>Body</strong>
          <br />
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            rows={16}
            style={{ width: "100%" }}
          />
        </label>
      </div>

      {edited && <p>You have edited this draft.</p>}
      {error && <p>Error: {error}</p>}

      <div style={{ marginTop: "12px" }}>
        <button onClick={() => handleDecision("approved")} disabled={saving}>
          Approve
        </button>{" "}
        <button onClick={() => handleDecision("rejected")} disabled={saving}>
          Reject
        </button>
      </div>
    </div>
  );
}

export default DraftReview;