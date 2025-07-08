import { Route, Routes } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import InfoPage from "./pages/InfoPage";
import { createUserId } from "./lib/user";

function App() {
  createUserId(); // create a user id if it doesn't exist
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/info" element={<InfoPage />} />
    </Routes>
  );
}

export default App;
