import { useState } from "react";
import "./MembersTab.css";
import plusIcon from "/assets/plus-icon.svg";
import editIcon from "/assets/edit-icon.svg";
import deleteIcon from "/assets/delete-icon.svg";
import showMoreIcon from "/assets/show-more-icon.svg"
import showLessIcon from "/assets/show-less-icon.svg"
import EditMemberModal from "./EditMemberModal";
import { API_URL } from "../lib/constants";
import ConfirmDeleteMember from "./ConfirmDeleteMember";

interface Props {
  groupId: string;
  members: string[];
  onUpdate?: (updated: string[]) => void;
}

function MembersTab({ groupId, members, onUpdate }: Props) {
  const [editableMembers, setEditableMembers] = useState(members);
  const [modalMode, setModalMode] = useState<"add" | "edit" | null>(null);
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  const [showMore, setShowMore] = useState(false);
  const [error, ] = useState("");
  const [deleteModalIndex, setDeleteModalIndex] = useState<number | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [modalError, setModalError] = useState("");

  const confirmDelete = async (index: number) => {
    const member = editableMembers[index];
    try {
      const res = await fetch(`${API_URL}/groups/${groupId}/members/${member}`, {
        method: "DELETE",
      });
      const data = await res.json();
      if (!res.ok) {
        setDeleteError(data.error || "Failed to delete member");
        return;
      }
  
      const updated = editableMembers.filter((_, i) => i !== index);
      setEditableMembers(updated);
      onUpdate?.(updated);
      setDeleteModalIndex(null);
      setDeleteError(null);
    } catch {
      setDeleteError("Network error");
    }
  };

  const visibleMembers = showMore ? editableMembers : editableMembers.slice(0, 5);

  const handleSaveMember = async (name: string) => {
    if (!/^[a-zA-Z0-9]+$/.test(name)) {
      setModalError("Only letters and numbers are allowed");
      return;
    }
    if (modalMode === "add") {
      try {
        const res = await fetch(`${API_URL}/groups/${groupId}/members`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username: name }),
        });
  
        const data = await res.json();
  
        if (!res.ok) {
          setModalError(data.error || "Failed to add member");
          return;
        }
  
        const updated = [...editableMembers, data.member_username];
        setEditableMembers(updated);
        onUpdate?.(updated);
        closeModal();
      } catch {
        setModalError("Network error");
      }
    } else if (modalMode === "edit" && selectedIndex !== null) {
      const oldName = editableMembers[selectedIndex];
  
      try {
        const res = await fetch(`${API_URL}/groups/${groupId}/members/${oldName}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ new_name: name }),
        });
  
        const data = await res.json();
  
        if (!res.ok || data.error) {
          setModalError(data.error || "Failed to update name");
          return; // 👈 importante
        }
  
        const updated = [...editableMembers];
        updated[selectedIndex] = name;
        setEditableMembers(updated);
        onUpdate?.(updated);
        closeModal();
      } catch {
        setModalError("Failed to update member name");
      }
    }
  };
  

  const handleDelete = (index: number) => {
    setDeleteModalIndex(index);
    setDeleteError(null); // limpiamos cualquier error previo
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
          onCancel={() => {
            closeModal();
            setModalError("");
          }}
          onSave={handleSaveMember}
          error={modalError}
        />
      )}

      {deleteModalIndex !== null && (
        <ConfirmDeleteMember
          memberName={editableMembers[deleteModalIndex]}
          onConfirm={() => confirmDelete(deleteModalIndex)}
          onCancel={() => {
            setDeleteModalIndex(null);
            setDeleteError(null);
          }}
          error={deleteError || undefined}
        />
      )}

    </div>
  );
}

export default MembersTab;
