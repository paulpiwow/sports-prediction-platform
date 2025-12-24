import { Link } from "react-router-dom";
import NbaPredictor from "../components/NbaPredictor";

export default function NbaPage() {
  return (
    <div className="soccer-page">
      <Link to="/" className="back-link">← Back</Link>

      <h1 style={{ textAlign: "center", marginBottom: "2rem" }}>
        🏀 NBA Predictor
      </h1>

      <NbaPredictor />
    </div>
  );
}

