const API_BASE = "http://127.0.0.1:8000";

export async function fetchAccounts() {
  const response = await fetch(`${API_BASE}/accounts`);
  if (!response.ok) throw new Error("Failed to fetch accounts");
  return response.json();
}

export async function fetchAccountDetail(accountId) {
  const response = await fetch(`${API_BASE}/accounts/${accountId}`);
  if (!response.ok) throw new Error("Failed to fetch account detail");
  return response.json();
}

export async function fetchDraft(accountId) {
  const response = await fetch(`${API_BASE}/accounts/${accountId}/draft`, {
    method: "POST",
  });
  if (!response.ok) throw new Error("Failed to fetch draft");
  return response.json();
}

export async function logDecision(accountId, payload) {
  const response = await fetch(`${API_BASE}/accounts/${accountId}/decision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to log decision");
  return response.json();
}
