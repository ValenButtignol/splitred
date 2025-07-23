import { useState } from "react";
import "./EditMemberModal.css";

interface Props {
  defaultValue?: string;
  onCancel: () => void;
  onSave: (name: string) => void;
  title: string;
  error?: string;
}

function EditMemberModal({ defaultValue = "", onCancel, onSave, title, error }: Props) {
  const [name, setName] = useState(defaultValue);

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h3>{title}</h3>
        <input
          type="text"
          placeholder="Enter name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="edit-member-input"
        />

        {error && <p className="delete-error">{error}</p>}

        <div className="modal-buttons">
          <button onClick={onCancel}>Cancel</button>
          <button onClick={() => onSave(name.trim())} disabled={!name.trim()}>
            Save
          </button>
        </div>
      </div>
    </div>
  );
}

export default EditMemberModal;
