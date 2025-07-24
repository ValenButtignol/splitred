import "./CreateGroupModal.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { API_URL } from "../lib/constants";

type Props = {
  onClose: () => void;
};

export default function CreateGroupModal({ onClose }: Props) {
  const [groupName, setGroupName] = useState("");
  const [memberInput, setMemberInput] = useState("");
  const [members, setMembers] = useState<string[]>([]);
  const navigate = useNavigate();

  const userId = localStorage.getItem("user_id");

  const handleAddMember = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && memberInput.trim() !== "") {
      e.preventDefault();
      if (!members.includes(memberInput.trim()) && /^[a-zA-Z0-9]+$/.test(memberInput)) {
        setMembers([...members, memberInput.trim()]);
        setMemberInput("");
      }
    }
  };

  const handleRemoveMember = (name: string) => {
    setMembers(members.filter((m) => m !== name));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (groupName.trim() === "") return;

    try {
      const res = await fetch(`${API_URL}/groups`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: groupName.trim(),
          owner_id: userId,
          members: members,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Unknown error");

      navigate(`/groups/${data.id}?owner_id=${userId}`);
      onClose();
    } catch (err) {
      alert("Error creating group: " + err);
    }
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

          <input
            type="text"
            placeholder="Add member and press Enter"
            value={memberInput}
            onChange={(e) => setMemberInput(e.target.value)}
            onKeyDown={handleAddMember}
            className="modal-input"
          />

          <div className="member-list">
            {members.map((member) => (
              <div key={member} className="member-chip">
                {member}
                <button
                  type="button"
                  className="remove-btn"
                  onClick={() => handleRemoveMember(member)}
                >
                  ✕
                </button>
              </div>
            ))}
          </div>

          <button type="submit" className="modal-button">
            Create
          </button>
        </form>
      </div>
    </div>
  );
}
