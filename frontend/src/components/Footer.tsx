import "./Footer.css";

import githubIcon from "../assets/github-icon.svg";
import linkedinIcon from "../assets/linkedin-icon.svg";

function Footer() {
  return (
    <footer className="footer">
      Made by Valentín Buttignol - <a href="https://github.com/ValenButtignol">
        <img src={githubIcon} alt="github-icon" className="github-icon" />
      </a> - <a href="https://www.linkedin.com/in/valenbuttignol/">
        <img src={linkedinIcon} alt="linkedin-icon" className="linkedin-icon" />
      </a>
    </footer>
  );
}

export default Footer;
