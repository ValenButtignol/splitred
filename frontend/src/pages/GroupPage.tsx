import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "./GroupPage.css";
import { API_URL } from "../lib/constants";
import Header from "../components/Header";
import Footer from "../components/Footer";
import GroupTabs from "../components/GroupTabs";
import ExpensesTab from "../components/ExpensesTab";
import MembersTab from "../components/MembersTab";
import SummaryTab from "../components/SummaryTab";
import ShareTab from "../components/ShareTab";

interface Payment {
  from: string;
  to: string;
  amount: number;
}
interface SummaryData {
  balances: { [member: string]: number };
  payments: Payment[];
}

interface Group {
  id: string;
  name: string;
  members: string[];
  owner_ids: string[];
}

interface Expense {
  id: string;
  description: string;
  creditors: { name: string; amount: number }[];
  debtors: string[];
  price: number;
}

function GroupPage() {
  const { group_id } = useParams();
  const [searchParams] = useSearchParams();
  const owner_id = searchParams.get("owner_id");
  const navigate = useNavigate();

  const [groupInfo, setGroupInfo] = useState<Group | null>(null);
  const [expenses, setExpenses] = useState<Expense[] | null>(null);
  const [members, setMembers] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState("expenses");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState<SummaryData | null>(null);
  const [initialLoad, setInitialLoad] = useState(true);

  const fetchMembers = async (groupId: string): Promise<string[]> => {
    const res = await fetch(`${API_URL}/groups/${groupId}/members`);
    if (!res.ok) throw new Error("Failed to fetch members");
    const data = await res.json();
    if (data.error) throw new Error(data.error);
    return data;
  };

  // Fetch main group info once
  useEffect(() => {
    if (!group_id || !owner_id) return;
  
    setInitialLoad(true);
    fetch(`${API_URL}/groups/${group_id}?owner_id=${owner_id}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) setError(data.error);
        else {
          setGroupInfo(data);
          setMembers(data.members);
        }
      })
      .catch(() => setError("Failed to load group"))
      .finally(() => setInitialLoad(false));
  }, [group_id, owner_id]);
  

  // Fetch tab-specific data
  useEffect(() => {
    if (!group_id) return;

    setLoading(true);
    setError(null);

    if (activeTab === "expenses") {
      fetch(`${API_URL}/groups/${group_id}/expenses`)
        .then((res) => res.json())
        .then((data) => {
          if (data.error) setError(data.error);
          else setExpenses(data);
        })
        .catch(() => setError("Failed to load expenses"))
        .finally(() => setLoading(false));
    }

    // Add future tab fetches here
    if (activeTab === "members") {
      fetchMembers(group_id)
        .then((data) => setMembers(data))
        .catch(() => setError("Failed to load members"))
        .finally(() => setLoading(false));
    }

    if (activeTab === "summary") {
      fetch(`${API_URL}/groups/${group_id}/summary`)
        .then((res) => res.json())
        .then((data) => {
          if (data.error) setError(data.error);
          else setSummary(data);
        })
        .catch(() => setError("Failed to load summary"))
        .finally(() => setLoading(false));
    }

    if (activeTab === "share") {
      setLoading(false);
    }

  }, [activeTab, group_id]);

  if (initialLoad) {
    return <div className="group-loading">Loading group...</div>;
  }
  
  if (error) {
    if (error === "Access denied: not an owner of this group") {
      navigate("/");
      return null;
    }
    return <div className="group-error">⚠️ {error || "Something went wrong"} ⚠️</div>;
  }
  
  if (!groupInfo) return null;  

  return (
    <div className="group-wrapper">
      <Header />
      <section className="group-page">
        <h2 className="group-title">{groupInfo.name}</h2>
        <div className="group-container">
          <GroupTabs activeTab={activeTab} setActiveTab={setActiveTab} />

          {loading && <p className="tab-placeholder">Loading...</p>}

          {!loading && activeTab === "expenses" && expenses && (
            <ExpensesTab expenses={expenses} groupId={group_id!} members={members} />
          )}

          {!loading && activeTab === "members" && (
            <MembersTab groupId={group_id!} members={members} />
          )}

          {!loading && activeTab === "summary" && summary && (
            <SummaryTab summary={summary} />
          )}

          {!loading && activeTab === "share" && (
            <ShareTab groupId={group_id!} ownerId={owner_id!} />
          )}
        </div>
      </section>
      <Footer />
    </div>
  );
}

export default GroupPage;
