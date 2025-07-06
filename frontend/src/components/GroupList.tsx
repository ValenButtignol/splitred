import "./GroupList.css";

function GroupList() {
  return (
    <section className="group-list">
      <h2 className="section-title">Expense Groups</h2>
      <div className="group-card">
        <p className="empty-text">You haven't created any group yet</p>
        <div className="group-buttons">
          <button className="circle-button">→</button>
          <button className="circle-button">+</button>
        </div>
      </div>
    </section>
  );
}

export default GroupList;
