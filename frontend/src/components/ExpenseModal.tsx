import { useState } from "react";
import "./ExpenseModal.css";
import plusIcon from "../assets/plus-icon.svg";
import deleteIcon from "../assets/delete-icon.svg";
import deleteIcon2 from "../assets/delete-icon2.svg";
import crossIcon from "../assets/cross-icon.svg";
import leftIcon from "../assets/left-icon.svg";
import rightIcon from "../assets/right-icon.svg";
import checkIcon from "../assets/check-icon.svg";

interface Props {
  onClose: () => void;
  onSubmit: (expense: {
    description: string;
    price: number;
    creditors: { name: string; amount: number }[];
    debtors: string[];
  }) => void;
  onDelete?: () => void;
  groupId: string;
  members: string[];
  editMode?: boolean;
  initialExpense?: {
    description: string;
    creditors: { name: string; amount: number }[];
    debtors: string[];
  };
}


function ExpenseModal({ onClose, onSubmit, onDelete, groupId, members, editMode, initialExpense }: Props) {
  const [step, setStep] = useState(1);
  const [description, setDescription] = useState(initialExpense?.description || "");
  const [creditors, setCreditors] = useState(initialExpense?.creditors || [{ name: "", amount: 0 }]);
  const [debtors, setDebtors] = useState(initialExpense?.debtors || []);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  
  const handleDelete = () => {
    setShowDeleteConfirm(true);
  }

  const confirmDelete = () => {
    if (onDelete) onDelete();
    onClose();
  };

  const cancelDelete = () => {
    setShowDeleteConfirm(false);
  };

  const toggleDebtor = (name: string) => {
    setDebtors((prev) =>
      prev.includes(name) ? prev.filter((d) => d !== name) : [...prev, name]
    );
  };

  const handleSubmit = () => {
    const total = creditors.reduce((sum, c) => sum + c.amount, 0);
    if (!description || total <= 0 || debtors.length === 0) {
      alert("Please complete all fields correctly.");
      return;
    }
    onSubmit({ description, price: total, creditors, debtors });
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
      <div className="modal-header">
        <h1 className="modal-title">{editMode ? "Edit Expense" : "Add Expense"}</h1>
        <button className="close-modal" onClick={onClose} style={{marginTop:"0.7rem"}}>
          <img src={crossIcon} alt="close-expense-addition" width={17} height={17} />
        </button>
      </div>

      <div className="stepper">
        {["Description", "Creditors", "Consumers", "Summary"].map((label, i) => (
          <div className={`step ${step === i + 1 ? "active" : ""}`} key={label}>
            <div className="step-indicator" />
            <span className="step-label">{label}</span>
          </div>
        ))}
      </div>

      {step === 1 && (
        <div className="step-content">
          <h2>Expense Description</h2>
          <input
            type="text"
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            style={{marginTop:"1rem"}}
          />
          <div className="modal-buttons">
            {editMode && (
              <button className="delete-expense-button" onClick={handleDelete}>
                <img src={deleteIcon2} alt="delete" width={17} height={17} />
              </button>
            )}
            <button disabled={!description} onClick={() => setStep(2)}>
              <img 
                src={rightIcon}
                width={17}
                height={17}
              />
            </button>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="step-content">
          <h2>Who paid and how much?</h2>
          {creditors.map((creditor, index) => (
            <div key={index} className="creditor-row">
              <select
                className="creditor-select"
                value={creditor.name}
                onChange={(e) => {
                  const updated = [...creditors];
                  updated[index].name = e.target.value;
                  setCreditors(updated);
                }}
              >
                <option value="" disabled>Select member</option>
                {members
                  .filter((m) => !creditors.some((c, i) => c.name === m && i !== index))
                  .map((member) => (
                    <option key={member} value={member}>
                      {member}
                    </option>
                  ))}
              </select>

              <input
                type="number"
                step="0.01"
                min="0"
                placeholder="$0.00"
                className="creditor-amount"
                value={creditor.amount === 0 ? "" : creditor.amount.toString()}
                onChange={(e) => {
                  const updated = [...creditors];
                  const val = parseFloat(e.target.value);
                  updated[index].amount = isNaN(val) || val < 0 ? 0 : val;
                  setCreditors(updated);
                }}
              />

              <button
                className="remove-creditor"
                onClick={() => {
                  setCreditors(creditors.filter((_, i) => i !== index));
                }}
              >
                <img src={deleteIcon} alt="remove-creditor-button" width={16} height={16} style={{marginTop:"2.5px"}} />
              </button>
            </div>
          ))}

          {members.length > creditors.length && (
            <button className="add-creditor" onClick={() => setCreditors([...creditors, { name: "", amount: 0 }])}>
              <img src={plusIcon} alt="add-creditor" width={16} height={16} />
              <span>Add Creditor</span>
            </button>
          )}

          <div className="modal-buttons">
            {editMode && (
              <button className="delete-expense-button" onClick={handleDelete}>
                <img src={deleteIcon2} alt="delete" width={17} height={17} />
              </button>
            )}
            <button onClick={() => setStep(1)}><img src={leftIcon} width={17} height={17} /></button>
            <button disabled={creditors.some((c) => !c.name || c.amount <= 0)} onClick={() => setStep(3)}>
              <img src={rightIcon} width={17} height={17} />
            </button>
          </div>
        </div>
      )}

      {step === 3 && (
        <div className="step-content">
          <h2>Who consumed this?</h2>
          <div className="members-list">
            {members.map((member) => (
              <label key={member}>
                <input
                  type="checkbox"
                  checked={debtors.includes(member)}
                  onChange={() => toggleDebtor(member)}
                />
                {member}
              </label>
            ))}
          </div>
          <div className="modal-buttons">
            {editMode && (
              <button className="delete-expense-button" onClick={handleDelete}>
                <img src={deleteIcon2} alt="delete" width={17} height={17} />
              </button>
            )}
            <button onClick={() => setStep(2)}>
              <img 
                src={leftIcon}
                width={17}
                height={17}
              />
            </button>
            <button disabled={debtors.length === 0} onClick={() => setStep(4)}>
              <img 
                src={rightIcon}
                width={17}
                height={17}
              />
            </button>
          </div>
        </div>
      )}

      {step === 4 && (
        <div className="step-content">
          <h2>{description}</h2>
          <hr className="summary-divider" />


          <div className="summary-section">
            <p className="summary-label">Creditors</p>
            <ul className="summary-list">
              {creditors.map((c) => (
                <li key={c.name}>
                  <span className="creditor-summary-name">{c.name}</span>
                  <span className="creditor-summary-amount">${c.amount.toFixed(2)}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="summary-section">
            <p className="summary-label">Consumers</p>
            <p>{debtors.join(", ")}</p> 
          </div>
          <hr className="summary-divider" />


          <div className="summary-section summary-total">
            <span className="summary-label">Total</span>
            <span className="creditor-summary-amount">
              ${creditors.reduce((s, c) => s + c.amount, 0).toFixed(2)}
            </span>
          </div>

          <div className="modal-buttons">
            {editMode && (
              <button className="delete-expense-button" onClick={handleDelete}>
                <img src={deleteIcon2} alt="delete" width={17} height={17} />
              </button>
            )}
            <button onClick={() => setStep(3)}>
              <img src={leftIcon} width={17} height={17} />
            </button>
            <button onClick={handleSubmit}>
              <img src={checkIcon} width={17} height={17} />
            </button>
          </div>
        </div>
      )}
      {showDeleteConfirm && (
        <div className="delete-confirmation">
          <p>Are you sure you want to delete this expense?</p>
          <div className="confirmation-buttons">
            <button onClick={cancelDelete}>No</button>
            <button onClick={confirmDelete}>Yes</button>
          </div>
        </div>
      )}
    </div>
  </div>
  );
}

export default ExpenseModal;
