from pathlib import Path
import pandas as pd

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Raw data path
RESULTS_PATH = BASE_DIR / "data" / "raw" / "results.csv"

df = pd.read_csv(RESULTS_PATH)

df["date"] = pd.to_datetime(df["date"], errors="coerce") #convert date to datetime

#Create a result column
def match_result(row):
    if row["home_score"] > row["away_score"]:
        return "home_win"
    elif row["home_score"] < row["away_score"]:
        return "away_win"
    else:
        return "draw"

#Look at each row and store winner in result column
df["result"] = df.apply(match_result, axis=1)

df = df[df["date"].dt.year >= 1950] #fliter to modern football

#Save cleaned data
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "clean_results.csv"
PROCESSED_PATH.parent.mkdir(exist_ok=True)
df.to_csv(PROCESSED_PATH, index=False)

print("Cleaned data saved:", PROCESSED_PATH)
