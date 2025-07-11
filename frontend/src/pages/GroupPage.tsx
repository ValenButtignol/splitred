// src/pages/GroupPage.tsx
import { useParams, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "./GroupPage.css";
import { API_URL } from "../lib/constants";

interface Group {
  id: string;
  name: string;
  members: string[];
  owner_ids: string[];
}

function GroupPage() {
  const { group_id } = useParams();
  const [searchParams] = useSearchParams();
  const owner_id = searchParams.get("owner_id");
  const [group, setGroup] = useState<Group | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!group_id || !owner_id) return;

    fetch(`${API_URL}${group_id}?owner_id=${owner_id}`)
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            setError(data.error);
        } else {
            setGroup(data);
        }
    })
    .catch(err => setError("Failed to load group"));
  }, [group_id, owner_id]);

  if (error) {
    return <div className="group-error">⚠️ {error}</div>;
  }

  if (!group) {
    return <div className="group-loading">Loading group...</div>;
  }

  return (
    <section className="group-page">
      <h1 className="group-title">{group.name}</h1>
      <h3 className="group-subtitle">Members</h3>
      <ul className="group-members">
        {group.members.map((member, i) => (
          <li key={i} className="group-member">{member}</li>
        ))}
      </ul>
    </section>
  );
}

export default GroupPage;
