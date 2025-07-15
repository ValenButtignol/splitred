import { useState } from "react";
import "./Header.css";
import { useNavigate } from "react-router-dom";
import FeedbackModal from "./FeedbackModal";
import splitredLogo from "../assets/splitred-logo.svg";
import infoIcon from "../assets/info-icon.svg";
import feedbackIcon from "../assets/feedback-icon.svg";;
import donateIcon from "../assets/donate-icon.svg";;

function Header() {
  const navigate = useNavigate();
  const [showFeedback, setShowFeedback] = useState(false);

  return (
    <header className="header">
      <button className="back-button" onClick={() => navigate("/")}>
        <h1 className="title">
          <img src={splitredLogo} alt="Splitred Logo" className="logo" />
          Splitred
        </h1>
      </button>
      <div className="icons-container">
        <img
          src={donateIcon}
          alt="donate-icon"
          className="donate-icon"
          onClick={() => navigate("/info")}
        />
        <img
          src={feedbackIcon}
          alt="feedback-icon"
          className="feedback-icon"
          onClick={() => setShowFeedback(true)}
        />
        <img
          src={infoIcon}
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
