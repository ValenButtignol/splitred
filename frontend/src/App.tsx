import { Route, Routes } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import InfoPage from "./pages/InfoPage";
import { createUserId } from "./lib/user";
import GroupPage from "./pages/GroupPage";

function App() {
  createUserId(); // create a user id if it doesn't exist
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/info" element={<InfoPage />} />
      <Route path="/groups/:group_id" element={<GroupPage />} />
    </Routes>
  );
}

export default App;
