from fastapi import FastAPI
import pandas as pd
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent

# Load model
model = joblib.load(BASE_DIR / "models" / "rf_model.pkl")

# Load team history
features_df = pd.read_csv(
    BASE_DIR / "data" / "processed" / "team_match_features.csv"
)

features_df["date"] = pd.to_datetime(features_df["date"])

FEATURE_COLS = [
    "is_home",
    "goals_for_rolling",
    "goals_against_rolling",
    "win_rolling"
]

app = FastAPI(title="Football Match Predictor")


#Create prediction endpoint
@app.get("/predict")
def predict(home_team: str, away_team: str):
    # Get latest stats for each team
    home_rows = features_df[features_df["team"] == home_team]
    away_rows = features_df[features_df["team"] == away_team]

    if home_rows.empty or away_rows.empty:
        return {
            "error": "One or both teams not found in dataset"
        }

    home_stats = home_rows.sort_values("date").iloc[-1]
    away_stats = away_rows.sort_values("date").iloc[-1]

    #Build feature vector for the home team
    home_input = [[
        1, #team is playing at home
        home_stats["goals_for_rolling"],
        home_stats["goals_against_rolling"],
        home_stats["win_rolling"]
    ]]
    #Build feature vector for the away team
    away_input = [[
        0, #team is playing away
        away_stats["goals_for_rolling"],
        away_stats["goals_against_rolling"],
        away_stats["win_rolling"]
    ]]

    # Use the trained model to predict win probabilities
    # predict_proba returns [P(loss), P(win)], so we take index [1]
    home_prob = model.predict_proba(home_input)[0][1]
    away_prob = model.predict_proba(away_input)[0][1]

    predicted_winner = home_team if home_prob > away_prob else away_team

    return {
        "home team" : home_team,
        "away_team": away_team,
        "home_win_prob": round(home_prob, 3),
        "away_win_prob": round(away_prob, 3),
        "predicted_winner": predicted_winner
    }

#Create teams endpoint
@app.get("/teams")
def get_teams():
    """
    Return a sorted list of all unique teams in the dataset.
    Used by the frontend to populate dropdowns.
    """
    teams = sorted(features_df["team"].unique().tolist())
    return teams

#Enable CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
