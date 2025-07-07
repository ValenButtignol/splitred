import "./InfoPage.css";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function InfoPage() {
  return (
    <div className="info-container">
      <Header />

      <div className="main-info">
        <section className="info-section">
        <h2 className="section-title" style={{ color: "#d3d3d3" }}>About Splitred</h2>
          <div className="info-card"> 
            <h2 className="section-title">What is Splitred?</h2>
            <p className="info-text">
              Splitred is a simple app to track and balance shared expenses with friends.
            </p>

            <h2 className="section-title">How it works?</h2>
            <ol className="info-list">
              <li>Create a group</li>
              <li>Add any member you want</li>
              <li>Add expenses with the added members</li>
              <li>Obtain who owes whom, minimizing the number of transactions.</li>
            </ol>

            <h2 className="section-title">Behind the algorithm</h2>
            <p className="info-text">
              Splitred calculates for each expense in the group, each person's net, and makes a balance.
              Then a greedy algorithm is used to split payments.
            </p>

            <h2 className="section-title">Example</h2>
            <ul className="info-list">
              <li>Alice pays $60 for Alice, Bob and Charlie.</li>
              <li>Bob pays $30 only for Alice and Bob.</li>
              <li>Charlie pays $0.</li>
            </ul>

            <pre className="info-text" style={{ marginLeft: "-0.5rem", textAlign: "center" }}>
Alice balance   = 60 - (60/3) - (30/2)   = 25 <br />
Bob balance     = - (60/3) - (30/2) + 30 = -5 <br />
Charlie balance = - (60/3)               = -20<br />
<br />
Alice pays 25 to Bob<br />
Bob pays 5 to Charlie<br />
Charlie pays 20 to Alice<br />
            </pre>
          </div>
        </section>
      </div>
      <Footer />
    </div>
  );
}
