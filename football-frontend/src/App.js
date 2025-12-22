import { useEffect, useState } from "react";
import "./App.css";

const countryToCode = {
  Argentina: "ar",
  Brazil: "br",
  Germany: "de",
  Ecuador: "ec",
  France: "fr",
  England: "gb-eng",
  Spain: "es",
  Italy: "it",
  Portugal: "pt",
  Netherlands: "nl",
};

function Flag({ team }) {
  if (!team || !countryToCode[team]) return null;

  return (
    <img
      src={`https://flagcdn.com/w40/${countryToCode[team]}.png`}
      alt={team}
      style={{ marginLeft: "10px", verticalAlign: "middle" }}
    />
  );
}

function App() {
  const [teams, setTeams] = useState([]);
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/teams")
      .then((res) => res.json())
      .then((data) => setTeams(data));
  }, []);

  const predictMatch = () => {
    if (!homeTeam || !awayTeam || homeTeam === awayTeam) {
      alert("Please select two different teams.");
      return;
    }

    fetch(
      `http://127.0.0.1:8000/predict?home_team=${homeTeam}&away_team=${awayTeam}`
    )
      .then((res) => res.json())
      .then((data) => setResult(data));
  };

  return (
    <div className="container">
      <div className="card">
        <h1>⚽ Football Match Predictor</h1>

        <div className="select-group">
          <label>Home Team</label>
          <div>
            <select value={homeTeam} onChange={(e) => setHomeTeam(e.target.value)}>
              <option value="">Select team</option>
              {teams.map((team) => (
                <option key={team} value={team}>
                  {team}
                </option>
              ))}
            </select>
            <Flag team={homeTeam} />
          </div>
        </div>

        <div className="select-group">
          <label>Away Team</label>
          <div>
            <select value={awayTeam} onChange={(e) => setAwayTeam(e.target.value)}>
              <option value="">Select team</option>
              {teams.map((team) => (
                <option key={team} value={team}>
                  {team}
                </option>
              ))}
            </select>
            <Flag team={awayTeam} />
          </div>
        </div>

        <button onClick={predictMatch}>Predict Match</button>

        {result && (
          <div className="result">
            <h2>Prediction Result</h2>
            <p><strong>Winner:</strong> {result.predicted_winner}</p>
            <p>Home Win Probability: {result.home_win_prob}</p>
            <p>Away Win Probability: {result.away_win_prob}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
