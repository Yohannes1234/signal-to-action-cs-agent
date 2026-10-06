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