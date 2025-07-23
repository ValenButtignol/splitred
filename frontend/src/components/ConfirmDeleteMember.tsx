import "./ConfirmDeleteMember.css";

interface Props {
  memberName: string;
  onConfirm: () => void;
  onCancel: () => void;
  error?: string;
}

function ConfirmDeleteMember({ memberName, onConfirm, onCancel, error }: Props) {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Remove Member</h2>
        <p className="delete-question">Are you sure you want to remove <strong>{memberName}</strong> from the group?</p>
        {error && <p className="delete-error">{error}</p>}
        <div className="modal-buttons">
          <button onClick={onCancel}>No</button>
          <button onClick={onConfirm}>Yes</button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmDeleteMember;
