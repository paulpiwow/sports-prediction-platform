from pathlib import Path
import pandas as pd

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_PATH = BASE_DIR / "data" / "processed" / "clean_results.csv"

# Load cleaned data
df = pd.read_csv(CLEAN_PATH)
df["date"] = pd.to_datetime(df["date"])

print("Loaded cleaned data")
print("Total matches:", len(df))
print("Date range:", df["date"].min(), "→", df["date"].max())
print(df["result"].value_counts())

# Create team-level match rows
# (one row per team per match creates a symmetric, ML-friendly dataset)

# Home team perspective
home_df = df[[
    "date", "home_team", "away_team",
    "home_score", "away_score", "result"
]].copy()

home_df["team"] = home_df["home_team"]
home_df["opponent"] = home_df["away_team"]
home_df["goals_for"] = home_df["home_score"]
home_df["goals_against"] = home_df["away_score"]
home_df["is_home"] = 1
home_df["win"] = home_df["result"] == "home_win"

# Away team perspective
away_df = df[[
    "date", "home_team", "away_team",
    "home_score", "away_score", "result"
]].copy()

away_df["team"] = away_df["away_team"]
away_df["opponent"] = away_df["home_team"]
away_df["goals_for"] = away_df["away_score"]
away_df["goals_against"] = away_df["home_score"]
away_df["is_home"] = 0
away_df["win"] = away_df["result"] == "away_win"

# Combine home + away rows
team_matches = pd.concat([home_df, away_df], ignore_index=True)
team_matches = team_matches.sort_values("date")

print("\nTeam-level match table created")
print(team_matches.head())

# Create rolling predictors
ROLLING_WINDOW = 5
rolling_cols = ["goals_for", "goals_against", "win"]

for col in rolling_cols:
    team_matches[f"{col}_rolling"] = (
        team_matches
        .groupby("team")[col]
        .rolling(ROLLING_WINDOW, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

print("\nRolling features created")
print(team_matches[
    ["team", "date", "goals_for_rolling", "goals_against_rolling", "win_rolling"]
].head(10))

# Save features for modeling
FEATURES_DIR = BASE_DIR / "data" / "processed"
FEATURES_PATH = FEATURES_DIR / "team_match_features.csv"

team_matches.to_csv(FEATURES_PATH, index=False)
print("\nSaved feature table to:", FEATURES_PATH)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

FEATURES_PATH = BASE_DIR / "data" / "processed" / "team_match_features.csv"
df = pd.read_csv(FEATURES_PATH)
df["date"] = pd.to_datetime(df["date"])

#Define what the model learns from
features = [
    "is_home",
    "goals_for_rolling",
    "goals_against_rolling",
    "win_rolling"
]

X = df[features]
y = df["win"].astype(int)

#Split by time, not randomly
train = df["date"] < "2018-01-01"
test = df["date"] >= "2018-01-01"

X_train, X_test = X[train], X[test]
y_train, y_test = y[train], y[test]

#Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

#Evaluate accuracy
preds = model.predict(X_test)
accuracy = accuracy_score(y_test, preds)

print("\nInitial model accuracy:", round(accuracy, 3))

baseline_preds = X_test["is_home"]
baseline_accuracy = accuracy_score(y_test, baseline_preds)

print("Baseline (home-only) accuracy:", round(baseline_accuracy, 3))
