import React, { useEffect, useState } from "react";

export default function NflPredictor() {
    const [teams, setTeams] = useState([]);
    const [homeTeam, setHomeTeam] = useState("");
    const [awayTeam, setAwayTeam] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/teams?sport=nfl")
            .then(res => res.json())
            .then(setTeams);
    }, []);

    const handlePredict = () => {
        setLoading(true);
        setResult(null);

        fetch(
            `http://127.0.0.1:8000/predict?sport=nfl&home_team=${homeTeam}&away_team=${awayTeam}`
        )
            .then(res => res.json())
            .then(data => {
                setResult(data);
                setLoading(false);
            });
    };

    const getLogo = (team) => {
        return `/nfl_logos/${team}.png`;
    };

    return (
        <div className="predictor-container">

            {/* TEAM SELECTION */}
            <div className="team-selection-grid">

                {/* HOME TEAM */}
                <div className="team-card">
                    <h3>Home Team</h3>
                    <select value={homeTeam} onChange={e => setHomeTeam(e.target.value)}>
                        <option value="">Select team</option>
                        {teams.map(t => (
                            <option key={t.id} value={t.name}>{t.name}</option>
                        ))}
                    </select>

                    {homeTeam && (
                        <img src={getLogo(homeTeam)} className="team-logo" alt={homeTeam} />
                    )}
                </div>

                {/* AWAY TEAM */}
                <div className="team-card">
                    <h3>Away Team</h3>
                    <select value={awayTeam} onChange={e => setAwayTeam(e.target.value)}>
                        <option value="">Select team</option>
                        {teams.map(t => (
                            <option key={t.id} value={t.name}>{t.name}</option>
                        ))}
                    </select>

                    {awayTeam && (
                        <img src={getLogo(awayTeam)} className="team-logo" alt={awayTeam} />
                    )}
                </div>
            </div>

            {/* PREDICT BUTTON */}
            <button
                className="predict-button"
                disabled={!homeTeam || !awayTeam || homeTeam === awayTeam || loading}
                onClick={handlePredict}
            >
                {loading ? "Predicting..." : "Predict Match"}
            </button>

            {/* RESULTS */}
            {result && (
                <div className="result-grid">

                    {/* WINNER */}
                    <div className="winner-card">
                        <h3>🏆 Predicted Winner</h3>
                        <img
                            src={getLogo(result.predicted_winner)}
                            className="winner-logo"
                            alt={result.predicted_winner}
                        />
                        <h2>{result.predicted_winner}</h2>
                    </div>

                    {/* MATCH BREAKDOWN */}
                    <div className="stats-card">
                        <h3>📊 Match Breakdown</h3>

                        <div className="team-block">
                            <p className="team-label">HOME TEAM</p>
                            <p className="team-name">{result.home_team}</p>
                        </div>

                        <div className="team-block">
                            <p className="team-label">AWAY TEAM</p>
                            <p className="team-name">{result.away_team}</p>
                        </div>


                        <div className="probability-block">
                            <p className="prob-label">Home Win Probability</p>
                            <div className="prob-bar">
                                <div
                                    className="prob-fill home"
                                    style={{ width: `${result.home_win_prob * 100}%` }}
                                />
                            </div>
                            <span className="prob-value">
                                {(result.home_win_prob * 100).toFixed(1)}%
                            </span>
                        </div>

                        <div className="probability-block">
                            <p className="prob-label">Away Win Probability</p>
                            <div className="prob-bar">
                                <div
                                    className="prob-fill away"
                                    style={{ width: `${result.away_win_prob * 100}%` }}
                                />
                            </div>
                            <span className="prob-value">
                                {(result.away_win_prob * 100).toFixed(1)}%
                            </span>
                        </div>
                    </div>



                </div>
            )}
        </div>
    );
}
