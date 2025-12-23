import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_PATH = BASE_DIR / "data" / "nba" / "raw" / "games.csv"
PROCESSED_DIR = BASE_DIR / "data" / "nba" / "processed"
PROCESSED_DIR.mkdir(exist_ok=True)

def clean_nba_data():
    df = pd.read_csv(RAW_PATH)

    # Drop games without final scores
    df = df.dropna(subset=["PTS_home", "PTS_away"])

    df["date"] = pd.to_datetime(df["GAME_DATE_EST"])

    # Home team rows
    home_df = pd.DataFrame({
        "date": df["date"],
        "team": df["HOME_TEAM_ID"],
        "opponent": df["VISITOR_TEAM_ID"],
        "points_for": df["PTS_home"],
        "points_against": df["PTS_away"],
        "is_home": 1
    })

    # Away team rows
    away_df = pd.DataFrame({
        "date": df["date"],
        "team": df["VISITOR_TEAM_ID"],
        "opponent": df["HOME_TEAM_ID"],
        "points_for": df["PTS_away"],
        "points_against": df["PTS_home"],
        "is_home": 0
    })

    team_games = pd.concat([home_df, away_df], ignore_index=True)
    team_games["win"] = (team_games["points_for"] > team_games["points_against"]).astype(int)

    team_games = team_games.sort_values(["team", "date"])

    out_path = PROCESSED_DIR / "team_games.csv"
    team_games.to_csv(out_path, index=False)

    print("Saved team-level NBA games to:", out_path)
    print(team_games.head())

if __name__ == "__main__":
    clean_nba_data()
