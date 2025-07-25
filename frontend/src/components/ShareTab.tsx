import { useState } from "react";
import "./ShareTab.css";
import copyIcon from "/assets/copy-icon.svg";

interface Props {
  groupId: string;
}

function ShareTab({ groupId }: Props) {
  const [copied, setCopied] = useState(false);

  const shareToken = `${groupId}`;

  const handleCopy = () => {
    navigator.clipboard.writeText(shareToken)
      .then(() => {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      })
      .catch((err) => {
        console.error("Failed to copy: ", err);
      });
  };

  return (
    <div className="share-tab">
      <p className="share-title">Share this group with your friends</p>
      <div className="share-box">
        <input
          type="text"
          readOnly
          value={shareToken}
          className="share-input"
          onClick={(e) => (e.target as HTMLInputElement).select()}
        />
          <button className="copy-button" onClick={handleCopy}>
            <img
              src={copyIcon}
              alt="copy-icon"
              width={25}
              height={25}
              style={{ marginTop: "0.2rem" }}
            />
            {copied && <span className="tooltip-copied">Copied!</span>}
          </button>
      </div>
      <p style={{color:"white", marginTop:"1rem"}}>Paste this token on the "Join" button in the Home page.</p>
      <p className="share-hint">Be careful, anyone with this token will be able to join and edit this group.</p>
    </div>
  );
}

export default ShareTab;
