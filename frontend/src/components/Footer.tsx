import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">
      Made by Valentín Buttignol - <a href="https://github.com/ValenButtignol">
        <img src={"./src/assets/github-icon.svg"} alt="github-icon" className="github-icon" />
      </a> - <a href="https://www.linkedin.com/in/valenbuttignol/">
        <img src={"./src/assets/linkedin-icon.svg"} alt="linkedin-icon" className="linkedin-icon" />
      </a>
    </footer>
  );
}

export default Footer;
