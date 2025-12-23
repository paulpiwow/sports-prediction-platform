import NbaPredictor from "../components/NbaPredictor";
import { Link } from "react-router-dom";

export default function NbaPage() {
  return (
    <div className="page">
      <Link to="/" className="back-link">← Back</Link>
      <h1>🏀 NBA Predictor</h1>
      <NbaPredictor />
    </div>
  );
}
