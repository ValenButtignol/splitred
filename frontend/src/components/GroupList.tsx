// GroupList.tsx
import "./GroupList.css";
import { useState, useEffect } from "react";
import CreateGroupModal from "./CreateGroupModal";
import JoinGroupModal from "./JoinGroupModal";
import { useNavigate } from "react-router-dom";

interface Group {
  id: string;
  name: string;
  members: string[];
  updated_at?: string;
}

function GroupList() {
  const [groups, setGroups] = useState<Group[]>([]);
  const [showCreateGroupModal, setShowCreateGroupModal] = useState(false);
  const [showJoinGroupModal, setShowJoinGroupModal] = useState(false);
  const [showMore, setShowMore] = useState(false);
  const navigate = useNavigate();
  const userId = localStorage.getItem("user_id");

  useEffect(() => {
    if (!userId) return;
  
    fetch(`http://localhost:5000/groups?owner_id=${userId}`)
      .then(res => res.json())
      .then(data => {
        const sorted = data.sort((a: Group, b: Group) =>
          (b.updated_at || '').localeCompare(a.updated_at || '')
        );
        setGroups(sorted);
      });
  }, []);
  

  const visibleGroups = showMore ? groups : groups.slice(0, 3);

  return (
    <section className="group-list">
      <h2 className="section-title">Expense Groups</h2>
      <div className="group-card">
        {groups.length === 0 ? (
          <p className="empty-text">You haven't created any group yet</p>
        ) : (
          <div className="group-preview-list">
            {visibleGroups.map((group) => (
              <button
                key={group.id}
                className="group-preview"
                onClick={() => navigate(`/groups/${group.id}?owner_id=${userId}`)}
              >
                <h2>{group.name}</h2>
                <div className="group-preview-members">
                  {group.members.slice(0, 3).join(", ")}
                  {group.members.length > 3 ? ", ..." : ""}
                </div>
              </button>
            ))}
          </div>
        )}

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

          {groups.length > 3 && (
            <button className="circle-button" onClick={() => setShowMore(!showMore)}>
              <img 
                src={
                  showMore
                    ? "./src/assets/show-less-icon.svg"
                    : "./src/assets/show-more-icon.svg"
                }
                alt={showMore ? "show-less-icon" : "show-more-icon"}
                width={17}
                height={17}
                style={{ marginTop: "0.2rem" }}
              />
            </button>
          )}

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
