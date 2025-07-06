import Header from "../components/Header";
import GroupList from "../components/GroupList";
import Footer from "../components/Footer";
import "./LandingPage.css";

function LandingPage() {
  return (
    <div className="home-container">
      <Header />
      <main className="main">
        <GroupList />
      </main>
      <Footer />
    </div>
  );
}

export default LandingPage;
