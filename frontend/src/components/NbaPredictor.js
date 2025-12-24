import React, { useEffect, useState } from "react";

// Helper: NBA logo by TEAM_ID
function getNbaLogo(teamId) {
  if (!teamId) return null;
  return `https://cdn.nba.com/logos/nba/${teamId}/primary/L/logo.svg`;
}

export default function NbaPredictor() {
  const [teams, setTeams] = useState([]);
  const [homeTeam, setHomeTeam] = useState(null);
  const [awayTeam, setAwayTeam] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch NBA teams
  useEffect(() => {
    fetch("http://127.0.0.1:8000/teams?sport=nba")
      .then(res => res.json())
      .then(setTeams)
      .catch(err => console.error("Failed to load NBA teams", err));
  }, []);

  const handlePredict = () => {
    if (!homeTeam || !awayTeam || homeTeam.id === awayTeam.id) return;

    setLoading(true);
    setResult(null);

    fetch(
      `http://127.0.0.1:8000/predict?sport=nba&home_team=${encodeURIComponent(
        homeTeam.name
      )}&away_team=${encodeURIComponent(awayTeam.name)}`
    )
      .then(res => res.json())
      .then(data => {
        setResult(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Prediction failed", err);
        setLoading(false);
      });
  };

  const winnerTeam = result
    ? teams.find(t => t.name === result.predicted_winner)
    : null;

  return (
    <>
      {/* TEAM SELECTION */}
      <div className="team-selection-grid">

        {/* HOME TEAM */}
        <div className="team-card">
          <h3>Home Team</h3>

          <select
            value={homeTeam?.id || ""}
            onChange={e =>
              setHomeTeam(
                teams.find(t => t.id === Number(e.target.value))
              )
            }
          >
            <option value="">Select team</option>
            {teams.map(team => (
              <option key={team.id} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>

          {homeTeam && (
            <img
              src={getNbaLogo(homeTeam.id)}
              alt={homeTeam.name}
              className="team-logo"
            />
          )}
        </div>

        {/* AWAY TEAM */}
        <div className="team-card">
          <h3>Away Team</h3>

          <select
            value={awayTeam?.id || ""}
            onChange={e =>
              setAwayTeam(
                teams.find(t => t.id === Number(e.target.value))
              )
            }
          >
            <option value="">Select team</option>
            {teams.map(team => (
              <option key={team.id} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>

          {awayTeam && (
            <img
              src={getNbaLogo(awayTeam.id)}
              alt={awayTeam.name}
              className="team-logo"
            />
          )}
        </div>
      </div>

      {/* PREDICT BUTTON */}
      <button
        className="predict-button"
        onClick={handlePredict}
        disabled={
          loading ||
          !homeTeam ||
          !awayTeam ||
          homeTeam.id === awayTeam.id
        }
      >
        {loading ? "Predicting..." : "Predict Match"}
      </button>

      {/* RESULTS */}
      {result && (
        <div className="result-grid">

          {/* WINNER CARD */}
          <div className="winner-card">
            <h3>🏆 Predicted Winner</h3>

            {winnerTeam && (
              <img
                src={getNbaLogo(winnerTeam.id)}
                alt={winnerTeam.name}
                className="winner-logo"
              />
            )}

            <h2>{result.predicted_winner}</h2>
          </div>

          {/* STATS CARD */}
          <div className="stats-card">
            <h3>Match Breakdown</h3>

            <p><strong>Home Team:</strong> {result.home_team}</p>
            <p><strong>Away Team:</strong> {result.away_team}</p>

            <p>
              <strong>Home Win Probability:</strong>{" "}
              {result.home_win_prob}
            </p>

            <p>
              <strong>Away Win Probability:</strong>{" "}
              {result.away_win_prob}
            </p>
          </div>
        </div>
      )}
    </>
  );
}

