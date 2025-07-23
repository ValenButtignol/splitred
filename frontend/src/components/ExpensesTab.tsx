// src/components/ExpensesTab.tsx

import "./ExpensesTab.css";
import { useEffect, useState } from "react";
import ExpenseModal from "./ExpenseModal";
import plusIcon from "../assets/plus-icon.svg";
import showMoreIcon from "../assets/show-more-icon.svg";
import showLessIcon from "../assets/show-less-icon.svg";
import { API_URL } from "../lib/constants";

interface Expense {
  id: string;
  description: string;
  creditors: { name: string; amount: number }[];
  debtors: string[];
  price: number;
}

interface Props {
  expenses: Expense[];
  groupId: string;
  members: string[];
}

function ExpensesTab({ expenses, groupId, members }: Props) {
  const [allExpenses, setAllExpenses] = useState<Expense[]>([]);
  const [visibleCount, setVisibleCount] = useState(5);
  const [showExpenseModal, setShowExpenseModal] = useState(false);
  const [expenseToEdit, setExpenseToEdit] = useState<Expense | null>(null);

  // Sync local expenses when parent data changes
  useEffect(() => {
    setAllExpenses(expenses);
  }, [expenses]);

  const handleAddExpense = async (expense: {
    description: string;
    price: number;
    creditors: { name: string; amount: number }[];
    debtors: string[];
  }) => {
    try {
      const res = await fetch(`${API_URL}/groups/${groupId}/expenses`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(expense),
      });
      
      console.log(res);

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Failed to create expense");
      }
  
      const newExpense = await res.json();
      setAllExpenses((prev) => [...prev, newExpense]);
    } catch (error) {
      console.error("Error adding expense:", error);
      alert(`Error: ${(error as Error).message}`);
    }
  };  

  const handleEditExpense = async (updatedExpense: {
    id: string;
    description: string;
    price: number;
    creditors: { name: string; amount: number }[];
    debtors: string[];
  }) => {
    try {
      const res = await fetch(
        `${API_URL}/expenses/${updatedExpense.id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            description: updatedExpense.description,
            price: updatedExpense.price,
            creditors: updatedExpense.creditors,
            debtors: updatedExpense.debtors,
          }),
        }
      );
  
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Failed to update expense");
      }
  
      const updated = await res.json();
  
      setAllExpenses((prev) =>
        prev.map((exp) => (exp.id === updated.id ? updated : exp))
      );
      setExpenseToEdit(null);
    } catch (error) {
      console.error("Error updating expense:", error);
      alert(`Error: ${(error as Error).message}`);
    }
  };

  const handleDeleteExpense = async (expenseId: string) => {
    try {
      const res = await fetch(`${API_URL}/expenses/${expenseId}`, {
        method: "DELETE",
      });
  
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Failed to delete expense");
      }
  
      setAllExpenses((prev) => prev.filter((e) => e.id !== expenseId));
      setExpenseToEdit(null);
    } catch (error) {
      console.error("Error deleting expense:", error);
      alert(`Error: ${(error as Error).message}`);
    }
  };
  

  const visibleExpenses = allExpenses.slice(0, visibleCount);

  return (
    <div className="expenses-container">
      {allExpenses.length === 0 ? (
        <div className="no-expenses-message">
          Looks like there are no expenses yet, press the button below to add one
        </div>
      ) : (
        <table className="expenses-table">
          <thead>
            <tr>
              <th style={{ textAlign: "center", width:"30%" }}>Description</th>
              <th style={{ textAlign: "center" }}>Creditors</th>
              <th style={{ textAlign: "center" }}>Consumers</th>
              <th style={{ textAlign: "center" }}>Price</th>
            </tr>
          </thead>
          <tbody>
            {visibleExpenses.map((expense) => (
              <tr
                key={expense.id}
                className="expense-row"
                onClick={() => setExpenseToEdit(expense)}
                style={{ cursor: "pointer" }}
              >
                <td style={{ wordBreak: "break-word", overflowWrap: "break-word" }}>
                  {
                    expense.description.length > 30 ? 
                    expense.description.slice(0, 30) + "..." : 
                    expense.description
                  }
                </td>
                <td>
                  {expense.creditors.map((c) => (
                    <div key={`${expense.id}-${c.name}`}>
                      {c.name}: ${c.amount}
                    </div>
                  ))}
                </td>
                <td>{expense.debtors.join(", ")}</td>
                <td>${expense.price.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
  
      <div className="expenses-buttons">
        {allExpenses.length > 5 && (
          <button
            className="circle-button"
            onClick={() =>
              setVisibleCount((prev) =>
                prev === 5 ? allExpenses.length : 5
              )
            }
          >
            <img
              src={visibleCount === 5 ? showMoreIcon : showLessIcon}
              alt={visibleCount === 5 ? "show-more-icon" : "show-less-icon"}
              width={17}
              height={17}
              className="icon-centered"
            />
          </button>
        )}
  
        <button className="circle-button" onClick={() => setShowExpenseModal(true)}>
          <img
            src={plusIcon}
            alt="add-expense-icon"
            width={17}
            height={17}
            className="icon-centered"
          />
        </button>
      </div>
  
      {showExpenseModal && (
        <ExpenseModal
          onClose={() => setShowExpenseModal(false)}
          onSubmit={handleAddExpense}
          members={members}
          groupId={groupId}
        />
      )}
      {expenseToEdit && (
        <ExpenseModal
          onClose={() => setExpenseToEdit(null)}
          onSubmit={(updated) =>
            handleEditExpense({ ...updated, id: expenseToEdit.id })
          }
          onDelete={() => handleDeleteExpense(expenseToEdit.id)}
          members={members}
          groupId={groupId}
          editMode={true}
          initialExpense={expenseToEdit}
        />
      )}

    </div>
  );  
}

export default ExpensesTab;
