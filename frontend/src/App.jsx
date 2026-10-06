import { useEffect, useState } from "react";
import { fetchAccounts } from "./api";
import "./App.css";

function App() {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAccounts()
      .then(setAccounts)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading accounts...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Accounts</h1>
      <table>
        <thead>
          <tr>
            <th>Account</th>
            <th>Risk</th>
            <th>Primary Driver</th>
          </tr>
        </thead>
        <tbody>
          {accounts.map((acc) => (
            <tr key={acc.account_id}>
              <td>{acc.account_name}</td>
              <td>{acc.risk_band}</td>
              <td>{acc.primary_driver}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;