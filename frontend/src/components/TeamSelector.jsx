import { useEffect, useState } from "react";
import { fetchTeams } from "../api";

export default function TeamSelector({ sport, onSelect }) {
  const [teams, setTeams] = useState([]);
  const [home, setHome] = useState("");
  const [away, setAway] = useState("");

  useEffect(() => {
    fetchTeams(sport).then(setTeams);
    setHome("");
    setAway("");
  }, [sport]);

  function handleSubmit(e) {
    e.preventDefault();
    if (home && away && home !== away) {
      onSelect(home, away);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <select value={home} onChange={(e) => setHome(e.target.value)}>
        <option value="">Select Home Team</option>
        {teams.map((t) => (
          <option key={t.id} value={t.id}>{t.name}</option>
        ))}
      </select>

      <select value={away} onChange={(e) => setAway(e.target.value)}>
        <option value="">Select Away Team</option>
        {teams.map((t) => (
          <option key={t.id} value={t.id}>{t.name}</option>
        ))}
      </select>

      <button type="submit">Predict</button>
    </form>
  );
}
