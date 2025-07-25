import "./CreateGroupModal.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { API_URL } from "../lib/constants";

type Props = {
  onClose: () => void;
};

export default function JoinGroupModal({ onClose }: Props) {
  const [groupIdInput, setGroupIdInput] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const groupId = groupIdInput.trim();
    const userId = localStorage.getItem("user_id");

    if (!groupId || !userId) {
      setError("Group ID and User ID are required.");
      return;
    }

    try {
      const res = await fetch(`${API_URL}/groups/${groupId}/join`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_id: userId }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Error joining group");
      }

      navigate(`/groups/${groupId}?owner_id=${userId}`);
      onClose();
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2 className="modal-title">Join a group</h2>
        <form onSubmit={handleSubmit} className="modal-form">
          <input
            type="text"
            placeholder="Enter group ID"
            value={groupIdInput}
            onChange={(e) => setGroupIdInput(e.target.value)}
            className="modal-input"
          />
          {error && <p className="delete-error">{error}</p>}
          <button type="submit" className="modal-button">
            Join
          </button>
        </form>
      </div>
    </div>
  );
}
