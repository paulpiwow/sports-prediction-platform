const BASE_URL = "http://127.0.0.1:8000";

export async function fetchTeams(sport) {
  const res = await fetch(`${BASE_URL}/teams?sport=${sport}`);
  return res.json();
}

export async function fetchPrediction(sport, homeTeam, awayTeam) {
  const params = new URLSearchParams({
    sport,
    home_team: homeTeam,
    away_team: awayTeam,
  });

  const res = await fetch(`${BASE_URL}/predict?${params.toString()}`);
  return res.json();
}
