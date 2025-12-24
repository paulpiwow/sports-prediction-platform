import { useEffect, useState } from "react";

export default function SoccerPredictor() {
  const [teams, setTeams] = useState([]);
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch soccer teams on mount
  useEffect(() => {
    fetch("http://127.0.0.1:8000/teams?sport=soccer")
      .then(res => res.json())
      .then(data => setTeams(data))
      .catch(err => console.error("Failed to load teams:", err));
  }, []);

  // Map team name -> flag code
  function getFlag(teamName) {
    const map = {
      Algeria: "dz",
      Brazil: "br",
      Germany: "de",
      England: "gb",
      France: "fr",
      Spain: "es",
      Italy: "it",
      Argentina: "ar",
      Portugal: "pt",
      Netherlands: "nl"
    };

    return map[teamName]
      ? `https://flagcdn.com/w160/${map[teamName]}.png`
      : "/globe.png";
  }

  async function handlePredict() {
    if (!homeTeam || !awayTeam || homeTeam === awayTeam) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/predict?sport=soccer&home_team=${homeTeam}&away_team=${awayTeam}`
      );
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Prediction failed:", err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {/* TEAM SELECTION */}
      <div className="team-selection-grid">

        {/* HOME TEAM */}
        <div className="team-card">
          <h3>Home Team</h3>

          <select
            value={homeTeam}
            onChange={e => setHomeTeam(e.target.value)}
          >
            <option value="">Select team</option>
            {teams.map(team => (
              <option key={team.id} value={team.name}>
                {team.name}
              </option>
            ))}
          </select>

          {homeTeam && (
            <img
              src={getFlag(homeTeam)}
              alt={homeTeam}
              className="team-image"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = "/globe.png";
              }}
            />
          )}

        </div>

        {/* AWAY TEAM */}
        <div className="team-card">
          <h3>Away Team</h3>

          <select
            value={awayTeam}
            onChange={e => setAwayTeam(e.target.value)}
          >
            <option value="">Select team</option>
            {teams.map(team => (
              <option key={team.id} value={team.name}>
                {team.name}
              </option>
            ))}
          </select>

          {awayTeam && (
            <img
              src={getFlag(awayTeam)}
              alt={awayTeam}
              className="team-image"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = "/globe.png";
              }}
            />
          )}

        </div>
      </div>

      {/* PREDICT BUTTON */}
      <button
        className="predict-button"
        onClick={handlePredict}
        disabled={loading || !homeTeam || !awayTeam || homeTeam === awayTeam}
      >
        {loading ? "Predicting..." : "Predict Match"}
      </button>

      {/* RESULT */}
      {result && (
        <div className="result-grid">

          {/* WINNER CARD */}
          <div className="winner-card">
            <h3>🏆 Predicted Winner</h3>

            <img
              src={getFlag(result.predicted_winner)}
              alt={result.predicted_winner}
              className="winner-flag"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = "/globe.png";
              }}
            />


            <h2>{result.predicted_winner}</h2>
          </div>

          {/* STATS CARD */}
          <div className="stats-card">
            <h3>📊 Match Breakdown</h3>

            {/* HOME TEAM */}
            <div className="stats-row">
              <div className="stats-label">Home Team</div>
              <div className="stats-value">{result.home_team}</div>
            </div>

            {/* AWAY TEAM */}
            <div className="stats-row">
              <div className="stats-label">Away Team</div>
              <div className="stats-value">{result.away_team}</div>
            </div>

            {/* HOME PROB */}
            <div className="stats-row">
              <div className="stats-label">Home Win Probability</div>
              <div
                className={`stats-value ${result.home_win_prob > result.away_win_prob ? "leading" : "trailing"
                  }`}
              >
                {(result.home_win_prob * 100).toFixed(1)}%
              </div>
              <div className="prob-bar">
                <div
                  className="prob-fill home"
                  style={{ width: `${result.home_win_prob * 100}%` }}
                />
              </div>
            </div>

            {/* AWAY PROB */}
            <div className="stats-row">
              <div className="stats-label">Away Win Probability</div>
              <div
                className={`stats-value ${result.away_win_prob > result.home_win_prob ? "leading" : "trailing"
                  }`}
              >
                {(result.away_win_prob * 100).toFixed(1)}%
              </div>
              <div className="prob-bar">
                <div
                  className="prob-fill away"
                  style={{ width: `${result.away_win_prob * 100}%` }}
                />
              </div>
            </div>
          </div>

        </div>
      )}

    </>
  );
}
