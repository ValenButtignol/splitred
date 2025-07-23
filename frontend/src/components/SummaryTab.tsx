import "./SummaryTab.css";

interface Payment {
  from: string;
  to: string;
  amount: number;
}

interface SummaryData {
  balances: { [member: string]: number };
  payments: Payment[];
}

interface Props {
  summary: SummaryData;
}

const SummaryTab: React.FC<Props> = ({ summary }) => {
  const paymentsByCreditor: { [creditor: string]: { from: string; amount: number }[] } = {};

  summary.payments.forEach(({ from, to, amount }) => {
    if (amount === 0) return;
    if (!paymentsByCreditor[to]) {
      paymentsByCreditor[to] = [];
    }
    paymentsByCreditor[to].push({ from, amount });
  });

  return (
    <div className="summary-tab">
      <h2 className="summary-title">Payments:</h2>
      {Object.entries(paymentsByCreditor).map(([creditor, debts]) => (
        <div className="creditor-block" key={creditor}>
          <p className="creditor-name">{creditor} is owed by:</p>
          <ul className="debtor-list">
            {debts.map(({ from, amount }) => (
              <li className="debtor-item" key={from}>
                {from}: <span className="amount">${amount.toFixed(2)}</span>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default SummaryTab;
