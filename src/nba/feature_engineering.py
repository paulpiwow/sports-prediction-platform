import pandas as pd
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_PATH = BASE_DIR / "data" / "nba" / "processed" / "team_games.csv"
OUTPUT_PATH = BASE_DIR / "data" / "nba" / "processed" / "team_features.csv"

ROLLING_WINDOW = 5  # last 5 games form

# Feature Engineering
def build_nba_features():
    df = pd.read_csv(INPUT_PATH)
    df["date"] = pd.to_datetime(df["date"])

    # Ensure correct sorting before rolling calculations
    df = df.sort_values(["team", "date"])

    # Rolling average points scored
    df["points_for_rolling"] = (
        df.groupby("team")["points_for"]
        .rolling(ROLLING_WINDOW)
        .mean()
        .reset_index(level=0, drop=True)
    )

    # Rolling average points allowed
    df["points_against_rolling"] = (
        df.groupby("team")["points_against"]
        .rolling(ROLLING_WINDOW)
        .mean()
        .reset_index(level=0, drop=True)
    )

    # Rolling win rate
    df["win_rate_rolling"] = (
        df.groupby("team")["win"]
        .rolling(ROLLING_WINDOW)
        .mean()
        .reset_index(level=0, drop=True)
    )

    # Rolling point differential
    df["point_diff_rolling"] = (
        df["points_for_rolling"] - df["points_against_rolling"]
    )

    # Drop rows where rolling window is incomplete
    df = df.dropna().reset_index(drop=True)

    # Save features
    df.to_csv(OUTPUT_PATH, index=False)

    print("NBA feature table saved to:")
    print(OUTPUT_PATH)
    print("\nFeature columns:")
    print(df.columns.tolist())
    print("\nSample rows:")
    print(df.head())

# Entry Point
if __name__ == "__main__":
    build_nba_features()
