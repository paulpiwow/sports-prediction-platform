import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  // ----- State -----
  const [sport, setSport] = useState("nba");
  const [teams, setTeams] = useState([]);
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // ----- Fetch teams whenever sport changes -----
  useEffect(() => {
    setLoading(true);
    setError(null);

    fetch(`http://127.0.0.1:8000/teams?sport=${sport}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch teams");
        }
        return res.json();
      })
      .then((data) => {
        setTeams(data);
        setHomeTeam("");
        setAwayTeam("");
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load teams");
      })
      .finally(() => setLoading(false));
  }, [sport]);

  // ----- Predict match -----
  const handlePredict = () => {
    if (!homeTeam || !awayTeam) {
      setError("Please select both teams");
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);

    fetch(
      `http://127.0.0.1:8000/predict?sport=${sport}&home_team=${homeTeam}&away_team=${awayTeam}`
    )
      .then((res) => {
        if (!res.ok) {
          throw new Error("Prediction failed");
        }
        return res.json();
      })
      .then((data) => setPrediction(data))
      .catch((err) => {
        console.error(err);
        setError("Prediction error");
      })
      .finally(() => setLoading(false));
  };

  // ----- UI -----
  return (
    <div className="App">
      <h1>Sports Match Predictor</h1>

      {/* Sport Selector */}
      <div className="control">
        <label>Sport</label>
        <select value={sport} onChange={(e) => setSport(e.target.value)}>
          <option value="nba">NBA</option>
          <option value="soccer">Soccer</option>
        </select>
      </div>

      {/* Team Selectors */}
      <div className="control">
        <label>Home Team</label>
        <select
          value={homeTeam}
          onChange={(e) => setHomeTeam(e.target.value)}
        >
          <option value="">Select team</option>
          {teams.map((team) => (
            <option key={team.id} value={team.name}>
              {team.name}
            </option>
          ))}
        </select>
      </div>

      <div className="control">
        <label>Away Team</label>
        <select
          value={awayTeam}
          onChange={(e) => setAwayTeam(e.target.value)}
        >
          <option value="">Select team</option>
          {teams.map((team) => (
            <option key={team.id} value={team.name}>
              {team.name}
            </option>
          ))}
        </select>
      </div>

      {/* Predict Button */}
      <button onClick={handlePredict} disabled={loading}>
        {loading ? "Loading..." : "Predict Match"}
      </button>

      {/* Errors */}
      {error && <p className="error">{error}</p>}

      {/* Prediction Result */}
      {prediction && (
        <div className="result">
          <h2>Prediction Result</h2>
          <p>
            <strong>Home Team:</strong> {prediction.home_team}
          </p>
          <p>
            <strong>Away Team:</strong> {prediction.away_team}
          </p>
          <p>
            <strong>Home Win Probability:</strong>{" "}
            {prediction.home_win_prob}
          </p>
          <p>
            <strong>Away Win Probability:</strong>{" "}
            {prediction.away_win_prob}
          </p>
          <p>
            <strong>Predicted Winner:</strong>{" "}
            {prediction.predicted_winner}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
