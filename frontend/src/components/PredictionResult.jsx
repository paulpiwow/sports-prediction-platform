export default function PredictionResult({ result }) {
  if (!result || result.error) {
    return result?.error ? <p>{result.error}</p> : null;
  }

  const homePct = Math.round(result.home_win_prob * 100);
  const awayPct = Math.round(result.away_win_prob * 100);

  return (
    <div className="result">
      <h3>Prediction</h3>

      <div>
        <strong>{result.home_team}</strong>
        <div className="bar">
          <div style={{ width: `${homePct}%` }}>{homePct}%</div>
        </div>
      </div>

      <div>
        <strong>{result.away_team}</strong>
        <div className="bar">
          <div style={{ width: `${awayPct}%` }}>{awayPct}%</div>
        </div>
      </div>

      <h4>Winner: {result.predicted_winner}</h4>
    </div>
  );
}
