import { useState } from "react";
import TeamSelector from "./components/TeamSelector";
import PredictionResult from "./components/PredictionResult";
import { fetchPrediction } from "./api";

export default function App() {
  const [sport, setSport] = useState("soccer");
  const [result, setResult] = useState(null);

  async function handlePredict(home, away) {
    const data = await fetchPrediction(sport, home, away);
    setResult(data);
  }

  return (
    <main>
      <h1>Sports Prediction Platform</h1>

      <select value={sport} onChange={(e) => setSport(e.target.value)}>
        <option value="soccer">Soccer</option>
        <option value="nba">NBA</option>
      </select>

      <TeamSelector sport={sport} onSelect={handlePredict} />
      <PredictionResult result={result} />
    </main>
  );
}
