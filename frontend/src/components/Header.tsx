import { useState } from "react";
import "./Header.css";
import { useNavigate } from "react-router-dom";
import FeedbackModal from "./FeedbackModal";

function Header() {
  const navigate = useNavigate();
  const [showFeedback, setShowFeedback] = useState(false);

  return (
    <header className="header">
      <button className="back-button" onClick={() => navigate("/")}>
        <h1 className="title">
          <img src={"./src/assets/splitred-logo.svg"} alt="Splitred Logo" className="logo" />
          Splitred
        </h1>
      </button>
      <div className="icons-container">
        <img
          src={"./src/assets/donate-icon.svg"}
          alt="donate-icon"
          className="donate-icon"
          onClick={() => navigate("/info")}
        />
        <img
          src={"./src/assets/feedback-icon.svg"}
          alt="feedback-icon"
          className="feedback-icon"
          onClick={() => setShowFeedback(true)}
        />
        <img
          src={"./src/assets/info-icon.svg"}
          alt="info-icon"
          className="info-icon"
          onClick={() => navigate("/info")}
          />
      </div>
      {showFeedback && <FeedbackModal onClose={() => setShowFeedback(false)} />}
    </header>
  );
}

export default Header;
