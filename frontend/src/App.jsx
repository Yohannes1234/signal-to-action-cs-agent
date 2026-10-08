import { Routes, Route } from "react-router-dom";
import AccountList from "./AccountList";
import AccountDetail from "./AccountDetail";
import "./App.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<AccountList />} />
      <Route path="/accounts/:accountId" element={<AccountDetail />} />
    </Routes>
  );
}

export default App;