from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_PATH = BASE_DIR / "data" / "processed" / "clean_results.csv"

df = pd.read_csv(CLEAN_PATH)
df["date"] = pd.to_datetime(df["date"])

#Checks
print("Total matches:", len(df))
print("Date range:", df["date"].min(), "→", df["date"].max())
print(df["result"].value_counts())

#Win rates by home/away
result_counts = df["result"].value_counts(normalize=True) * 100
print("\nOverall result distribution (%):")
print(result_counts.round(2))

#Compute total matches and win rates per team
home = df[["home_team", "result"]].copy()   #create smaller DF with only home_team
home["team"] = home["home_team"]
home["is_win"] = home["result"] == "home_win" #true if home team won, false otherwise

away = df[["away_team", "result"]].copy()
away["team"] = away["away_team"]
away["is_win"] = away["result"] == "away_win"

team_results = pd.concat([home[["team", "is_win"]],
                          away[["team", "is_win"]]])

team_summary = (
    team_results
    .groupby("team")    #group all rows by team name
    .agg(
        matches=("is_win", "count"), #compute number of rows per team
        wins=("is_win", "sum") #compute sum of True values
    )
)

team_summary["win_rate"] = team_summary["wins"] / team_summary["matches"] #compute win rate
team_summary = team_summary.sort_values("matches", ascending=False)

print(team_summary.head(10))

#Save analysis outputs
ANALYSIS_DIR = BASE_DIR / "data" / "analysis"
ANALYSIS_DIR.mkdir(exist_ok=True)

team_summary.to_csv(ANALYSIS_DIR / "team_win_rates.csv")
result_counts.to_csv(ANALYSIS_DIR / "overall_result_distribution.csv")

print("Analysis complete")
