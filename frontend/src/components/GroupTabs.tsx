import "./GroupTabs.css";

interface Props {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

function GroupTabs({ activeTab, setActiveTab }: Props) {
  const tabs = ["expenses", "summary", "members", "share"];

  return (
    <div className="group-tabs">
      {tabs.map((tab) => (
        <button
          key={tab}
          className={`tab-button ${activeTab === tab ? "active" : ""}`}
          onClick={() => setActiveTab(tab)}
        >
          {tab.charAt(0).toUpperCase() + tab.slice(1)}
        </button>
      ))}
    </div>
  );
}

export default GroupTabs;
