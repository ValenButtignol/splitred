import { useState } from "react";
import "./MembersTab.css";
import plusIcon from "../assets/plus-icon.svg";
import editIcon from "../assets/edit-icon.svg";
import deleteIcon from "../assets/delete-icon.svg";
import showMoreIcon from "../assets/show-more-icon.svg"
import showLessIcon from "../assets/show-less-icon.svg"
import EditMemberModal from "./EditMemberModal";

interface Props {
  members: string[];
  expenses: {
    creditors: { name: string }[];
    debtors: string[];
  }[];
  onUpdate?: (updated: string[]) => void;
}

// TODO: Terminar backend de esto.
function MembersTab({ members, expenses, onUpdate }: Props) {
  const [editableMembers, setEditableMembers] = useState(members);
  const [modalMode, setModalMode] = useState<"add" | "edit" | null>(null);
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  const [showMore, setShowMore] = useState(false);
  const [error, setError] = useState("");

  const visibleMembers = showMore ? editableMembers : editableMembers.slice(0, 5);

  const handleSaveMember = (name: string) => {
    if (modalMode === "add") {
      const updated = [...editableMembers, name];
      setEditableMembers(updated);
      onUpdate?.(updated);
    } else if (modalMode === "edit" && selectedIndex !== null) {
      const updated = [...editableMembers];
      updated[selectedIndex] = name;
      setEditableMembers(updated);
      onUpdate?.(updated);
    }

    closeModal();
  };

  const handleDelete = (index: number) => {
    const name = editableMembers[index];
    const used = expenses.some(
      (exp) =>
        exp.creditors.some((c) => c.name === name) ||
        exp.debtors.includes(name)
    );
    if (used) {
      setError(
        "This member cannot be deleted because they are involved in at least one expense."
      );
      setTimeout(() => setError(""), 4000);
      return;
    }

    const updated = editableMembers.filter((_, i) => i !== index);
    setEditableMembers(updated);
    onUpdate?.(updated);
  };

  const closeModal = () => {
    setModalMode(null);
    setSelectedIndex(null);
  };

  return (
    <div className="members-tab">
      <h3 className="members-title">Group Members</h3>
      {error && <p className="delete-error">{error}</p>}

      <ul className="members-list">
        {visibleMembers.map((member, index) => (
          <li key={index} className="member-item">
            <span>{member}</span>
            <div className="member-actions">
              <button
                className="member-options-button"
                onClick={() => {
                  setModalMode("edit");
                  setSelectedIndex(index);
                }}
              >
                <img src={editIcon} alt="edit" width={14} height={14} />
              </button>
              <button className="member-options-button" onClick={() => handleDelete(index)}>
                <img src={deleteIcon} alt="delete" width={14} height={14} />
              </button>
            </div>
          </li>
        ))}
      </ul>

      <div className="members-controls">
        {editableMembers.length > 5 && (
          <button className="circle-button" onClick={() => setShowMore(!showMore)}>
            <img 
              src={showMore ? showLessIcon : showMoreIcon}
              alt={showMore ? "show-less-icon" : "show-more-icon"}
              width={17}
              height={17}
              style={{ marginTop: "0.2rem" }}
            />
          </button>
        )}

        <button
          className="circle-button"
          onClick={() => setModalMode("add")}
        >
          <img src={plusIcon} alt="add" width={17} height={17} />
        </button>
      </div>

      {modalMode && (
        <EditMemberModal
          title={modalMode === "add" ? "Add Member" : "Edit Member"}
          defaultValue={
            modalMode === "edit" && selectedIndex !== null
              ? editableMembers[selectedIndex]
              : ""
          }
          onCancel={closeModal}
          onSave={handleSaveMember}
        />
      )}
    </div>
  );
}

export default MembersTab;
