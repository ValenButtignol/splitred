import "./CreateGroupModal.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

type Props = {
  onClose: () => void;
};

export default function JoinGroupModal({ onClose }: Props) {
  const [invitationLink, setInvitationLink] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (invitationLink.trim() === "") return;

    // TODO: Acá podrías hacer un POST al backend y obtener un ID real
    const fakeGroupId = encodeURIComponent(invitationLink.trim());

    navigate(`/group/${fakeGroupId}`);
    onClose();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2 className="modal-title">Join a group</h2>
        <form onSubmit={handleSubmit} className="modal-form">
          <input
            type="text"
            placeholder="Invitation link"
            value={invitationLink}
            onChange={(e) => setInvitationLink(e.target.value)}
            className="modal-input"
          />
          <button type="submit" className="modal-button">
            Join
          </button>
        </form>
      </div>
    </div>
  );
}
