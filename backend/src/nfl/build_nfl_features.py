import os
import pandas as pd


RAW_PATH = os.path.join("backend", "data", "nfl", "raw", "spreadspoke_scores.csv")
OUT_DIR = os.path.join("backend", "data", "nfl", "processed")
OUT_PATH = os.path.join(OUT_DIR, "team_games.csv")


def build_nfl_features():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(
            f"Could not find raw NFL CSV at:\n  {RAW_PATH}\n\n"
            f"Put your file there, or update RAW_PATH in build_nfl_features.py"
        )

    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(RAW_PATH)

    # --- Clean + normalize ---
    df = df.copy()

    # Parse date safely (dataset sometimes uses M/D/YYYY strings)
    df["schedule_date"] = pd.to_datetime(df["schedule_date"], errors="coerce")

    # Only keep rows with valid scores (avoid weird missing rows)
    df = df.dropna(subset=["schedule_date", "score_home", "score_away", "team_home", "team_away"])

    # Ensure numeric scores
    df["score_home"] = pd.to_numeric(df["score_home"], errors="coerce")
    df["score_away"] = pd.to_numeric(df["score_away"], errors="coerce")
    df = df.dropna(subset=["score_home", "score_away"])

    # Convert to int (NFL scores are integers)
    df["score_home"] = df["score_home"].astype(int)
    df["score_away"] = df["score_away"].astype(int)

    # --- Create TEAM-GAME rows (2 rows per game: one for each team) ---
    home_rows = pd.DataFrame({
        "date": df["schedule_date"],
        "season": df["schedule_season"],
        "team": df["team_home"],
        "opponent": df["team_away"],
        "points_for": df["score_home"],
        "points_against": df["score_away"],
        "is_home": 1
    })

    away_rows = pd.DataFrame({
        "date": df["schedule_date"],
        "season": df["schedule_season"],
        "team": df["team_away"],
        "opponent": df["team_home"],
        "points_for": df["score_away"],
        "points_against": df["score_home"],
        "is_home": 0
    })

    team_games = pd.concat([home_rows, away_rows], ignore_index=True)

    # Win label
    team_games["win"] = (team_games["points_for"] > team_games["points_against"]).astype(int)

    # Sort so rolling windows are correct
    team_games = team_games.sort_values(["team", "date"]).reset_index(drop=True)

    # --- Rolling features (like NBA style) ---
    window = 5  # you can change later

    team_games["points_for_rolling"] = (
        team_games.groupby("team")["points_for"]
        .transform(lambda s: s.rolling(window, min_periods=1).mean())
    )

    team_games["points_against_rolling"] = (
        team_games.groupby("team")["points_against"]
        .transform(lambda s: s.rolling(window, min_periods=1).mean())
    )

    team_games["win_rate_rolling"] = (
        team_games.groupby("team")["win"]
        .transform(lambda s: s.rolling(window, min_periods=1).mean())
    )

    team_games["point_diff_rolling"] = (
        team_games["points_for_rolling"] - team_games["points_against_rolling"]
    )

    # Keep only what we need for modeling + API
    keep_cols = [
        "date", "season", "team", "opponent", "is_home", "win",
        "points_for_rolling", "points_against_rolling", "win_rate_rolling", "point_diff_rolling"
    ]
    team_games = team_games[keep_cols]

    team_games.to_csv(OUT_PATH, index=False)

    print("✅ NFL features built!")
    print(f"Raw input:  {RAW_PATH}")
    print(f"Output:     {OUT_PATH}")
    print(f"Rows:       {len(team_games):,}")
    print("Columns:", list(team_games.columns))


if __name__ == "__main__":
    build_nfl_features()
