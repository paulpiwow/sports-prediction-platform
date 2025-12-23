import SoccerPredictor from "../components/SoccerPredictor";
import { Link } from "react-router-dom";

export default function SoccerPage() {
  return (
    <div className="page">
      <Link to="/" className="back-link">← Back</Link>
      <h1>⚽ Soccer Predictor</h1>
      <SoccerPredictor />
    </div>
  );
}
