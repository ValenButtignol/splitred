import "./CreateGroupModal.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

type Props = {
  onClose: () => void;
};

export default function CreateGroupModal({ onClose }: Props) {
  const [groupName, setGroupName] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (groupName.trim() === "") return;

    // Acá podrías hacer un POST al backend y obtener un ID real
    const fakeGroupId = encodeURIComponent(groupName.trim());

    navigate(`/group/${fakeGroupId}`);
    onClose();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2 className="modal-title">Create a new group</h2>
        <form onSubmit={handleSubmit} className="modal-form">
          <input
            type="text"
            placeholder="Group name"
            value={groupName}
            onChange={(e) => setGroupName(e.target.value)}
            className="modal-input"
          />
          <button type="submit" className="modal-button">
            Create
          </button>
        </form>
      </div>
    </div>
  );
}
