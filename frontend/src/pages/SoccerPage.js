import { Link } from "react-router-dom";
import SoccerPredictor from "../components/SoccerPredictor";

export default function SoccerPage() {
  return (
    <div className="page">
      <Link to="/" className="back-link">← Back</Link>

      <h1 className="page-title">
        ⚽ Soccer Predictor
      </h1>

      <SoccerPredictor />
    </div>
  );
}
