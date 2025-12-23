import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_PATH = BASE_DIR / "data" / "nba" / "raw" / "games.csv"

def load_nba_games():
    df = pd.read_csv(RAW_PATH)
    print("Loaded NBA games:", df.shape)
    print(df.head())
    return df

if __name__ == "__main__":
    load_nba_games()
