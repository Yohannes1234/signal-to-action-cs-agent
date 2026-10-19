const API_BASE = "http://127.0.0.1:8000";

async function request(path, options, fallbackMessage) {
  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, options);
  } catch {
    // Network failure: backend not running or unreachable
    throw new Error(
      "Can't reach the server. Make sure the backend is running and try again."
    );
  }

  if (!response.ok) {
    let message = fallbackMessage;
    try {
      const data = await response.json();
      if (typeof data.detail === "string") message = data.detail;
    } catch {
      // Response wasn't JSON; keep the fallback message
    }
    throw new Error(message);
  }

  return response.json();
}

export function fetchAccounts() {
  return request("/accounts", undefined, "Failed to load accounts.");
}

export function fetchAccountDetail(accountId) {
  return request(
    `/accounts/${accountId}`,
    undefined,
    "Failed to load this account."
  );
}

export function fetchDraft(accountId) {
  return request(
    `/accounts/${accountId}/draft`,
    { method: "POST" },
    "The AI draft could not be generated. Please try again."
  );
}

export function logDecision(accountId, payload) {
  return request(
    `/accounts/${accountId}/decision`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    },
    "Failed to record your decision. Please try again."
  );
}