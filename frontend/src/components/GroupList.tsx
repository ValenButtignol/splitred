import "./GroupList.css";
import { useState } from "react";
import CreateGroupModal from "./CreateGroupModal";
import JoinGroupModal from "./JoinGroupModal";

function GroupList() {
  const [showCreateGroupModal, setShowCreateGroupModal] = useState(false);
  const [showJoinGroupModal, setShowJoinGroupModal] = useState(false);
  return (
    <section className="group-list">
      <h2 className="section-title">Expense Groups</h2>
      <div className="group-card">
        <p className="empty-text">You haven't created any group yet</p>
        <div className="group-buttons">
          <button className="circle-button" onClick={() => setShowJoinGroupModal(true)}>
            <img 
              src={"./src/assets/join-icon.svg"} 
              alt="join-icon"
              width={17}
              height={17}
              style={{ marginTop: "0.2rem", marginRight: "0.15rem" }}
            />
          </button>
          <button className="circle-button" onClick={() => setShowCreateGroupModal(true)}>
            <img
              src={"./src/assets/plus-icon.svg"}
              alt="create-group-icon"
              width={17}
              height={17}
              style={{ marginTop: "0.2rem" }}
            />
          </button>
        </div>
      {showCreateGroupModal && <CreateGroupModal onClose={() => setShowCreateGroupModal(false)} />}
      {showJoinGroupModal && <JoinGroupModal onClose={() => setShowJoinGroupModal(false)} />}
      </div>
    </section>
  );
}

export default GroupList;
