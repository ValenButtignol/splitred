import { Route, Routes } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import InfoPage from "./pages/InfoPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/info" element={<InfoPage />} />
    </Routes>
  );
}

export default App;
