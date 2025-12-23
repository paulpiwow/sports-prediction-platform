import React, { useEffect, useState } from "react";

export default function NbaPredictor() {
  const [teams, setTeams] = useState([]);
  const [home, setHome] = useState("");
  const [away, setAway] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/teams?sport=nba")
      .then(res => res.json())
      .then(setTeams);
  }, []);

  const predict = () => {
    fetch(
      `http://127.0.0.1:8000/predict?sport=nba&home_team=${home}&away_team=${away}`
    )
      .then(res => res.json())
      .then(setResult);
  };

  return (
    <div className="predictor-card nba">
      <h2>🏀 NBA Predictor</h2>

      <select onChange={e => setHome(e.target.value)}>
        <option value="">Home Team</option>
        {teams.map(t => (
          <option key={t.id} value={t.name}>{t.name}</option>
        ))}
      </select>

      <select onChange={e => setAway(e.target.value)}>
        <option value="">Away Team</option>
        {teams.map(t => (
          <option key={t.id} value={t.name}>{t.name}</option>
        ))}
      </select>

      <button onClick={predict}>Predict Match</button>

      {result && (
        <div className="result">
          <p><strong>Winner:</strong> {result.predicted_winner}</p>
          <p>Home Win: {result.home_win_prob}</p>
          <p>Away Win: {result.away_win_prob}</p>
        </div>
      )}
    </div>
  );
}
