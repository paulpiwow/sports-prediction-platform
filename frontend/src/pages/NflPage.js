import { Link } from "react-router-dom";
import NflPredictor from "../components/NflPredictor";

export default function NflPage() {
  return (
    <div className="page">
      <Link to="/" className="back-link">← Back</Link>
      <h1>🏈 NFL Predictor</h1>
      <NflPredictor />
    </div>
  );
}
