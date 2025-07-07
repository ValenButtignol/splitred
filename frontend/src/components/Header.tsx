import "./Header.css";
import { useNavigate } from "react-router-dom";

function Header() {
  const navigate = useNavigate();

  return (
    <header className="header">
      <button className="back-button" onClick={() => navigate("/")}>
        <h1 className="title">
          <img src={"./src/assets/splitred-logo.svg"} alt="Splitred Logo" className="logo" />
          Splitred
        </h1>
      </button>
      <img
        src={"./src/assets/info-icon.svg"}
        alt="info-icon"
        className="info-icon"
        onClick={() => navigate("/info")}
        style={{ cursor: "pointer" }}
      />
    </header>
  );
}

export default Header;
