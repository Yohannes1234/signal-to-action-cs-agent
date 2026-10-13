import { Routes, Route } from "react-router-dom";
import AccountList from "./AccountList";
import AccountDetail from "./AccountDetail";
import DraftReview from "./DraftReview";
import "./App.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<AccountList />} />
      <Route path="/accounts/:accountId" element={<AccountDetail />} />
      <Route path="/accounts/:accountId/review" element={<DraftReview />} />
    </Routes>
  );
}

export default App;