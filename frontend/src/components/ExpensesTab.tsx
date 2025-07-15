// src/components/ExpensesTab.tsx

import "./ExpensesTab.css";
import { useEffect, useState } from "react";
import AddExpenseModal from "./AddExpenseModal";
import plusIcon from "../assets/plus-icon.svg";
import showMoreIcon from "../assets/show-more-icon.svg";
import showLessIcon from "../assets/show-less-icon.svg";

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

  // Sync local expenses when parent data changes
  useEffect(() => {
    setAllExpenses(expenses);
  }, [expenses]);

  const handleAddExpense = (expense: {
    description: string;
    price: number;
    creditors: { name: string; amount: number }[];
    debtors: string[];
  }) => {
    const newExpense: Expense = {
      ...expense,
      id: crypto.randomUUID(), // temporal
    };
    setAllExpenses((prev) => [...prev, newExpense]);
  };

  const visibleExpenses = allExpenses.slice(0, visibleCount);

  return (
    <div className="expenses-container">
      <table className="expenses-table">
        <thead>
          <tr>
            <th style={{ textAlign: "center" }}>Description</th>
            <th style={{ textAlign: "center" }}>Creditors</th>
            <th style={{ textAlign: "center" }}>Consumers</th>
            <th style={{ textAlign: "center" }}>Price</th>
          </tr>
        </thead>
        <tbody>
          {visibleExpenses.map((expense) => (
            <tr key={expense.id} className="expense-row">
              <td>{expense.description}</td>
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
        <AddExpenseModal
          onClose={() => setShowExpenseModal(false)}
          onSubmit={handleAddExpense}
          members={members}
          groupId={groupId}
        />
      )}
    </div>
  );
}

export default ExpensesTab;
