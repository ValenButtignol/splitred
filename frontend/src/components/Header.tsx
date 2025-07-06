import "./Header.css";

function Header() {
  return (
    <header className="header">
      <h1 className="title">
        <img src={"./src/assets/splitred-logo.svg"} alt="Splitred Logo" className="logo" />
        Splitred
      </h1>
      <div className="info-icon">ℹ️</div>
    </header>
  );
}

export default Header;
