from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#Enable CORS
app = FastAPI(title="Sports Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from pathlib import Path
import pandas as pd
import joblib


# Base paths
BASE_DIR = Path(__file__).resolve().parents[1]

# SOCCER: model + data
SOCCER_MODEL_PATH = BASE_DIR / "models" / "soccer" / "rf_model.pkl"
SOCCER_FEATURES_PATH = BASE_DIR / "data" / "soccer" / "processed" / "team_match_features.csv"

soccer_model = joblib.load(SOCCER_MODEL_PATH)
soccer_features = pd.read_csv(SOCCER_FEATURES_PATH)
soccer_features["date"] = pd.to_datetime(soccer_features["date"])

# NBA: model + data
NBA_MODEL_PATH = BASE_DIR / "models" / "nba" / "rf_model.pkl"
NBA_FEATURES_PATH = BASE_DIR / "data" / "nba" / "processed" / "team_features.csv"
NBA_TEAMS_PATH = BASE_DIR / "data" / "nba" / "raw" / "teams.csv"

nba_model = joblib.load(NBA_MODEL_PATH)
nba_features = pd.read_csv(NBA_FEATURES_PATH)
nba_features["date"] = pd.to_datetime(nba_features["date"])
nba_teams_df = pd.read_csv(NBA_TEAMS_PATH)

# NFL assets
nfl_features = pd.read_csv(
    BASE_DIR / "data/nfl/processed/team_games.csv",
    parse_dates=["date"]
)

nfl_model = joblib.load(
    BASE_DIR / "models/nfl_model.pkl"
)


# SOCCER prediction helper
def predict_soccer_match(home_team: str, away_team: str):
    home_rows = soccer_features[soccer_features["team"] == home_team]
    away_rows = soccer_features[soccer_features["team"] == away_team]

    if home_rows.empty or away_rows.empty:
        raise ValueError("One or both soccer teams not found")

    home_latest = home_rows.sort_values("date").iloc[-1]
    away_latest = away_rows.sort_values("date").iloc[-1]

    home_input = [[
        1,
        home_latest["goals_for_rolling"],
        home_latest["goals_against_rolling"],
        home_latest["win_rolling"]
    ]]

    away_input = [[
        0,
        away_latest["goals_for_rolling"],
        away_latest["goals_against_rolling"],
        away_latest["win_rolling"]
    ]]

    home_prob = soccer_model.predict_proba(home_input)[0][1]
    away_prob = soccer_model.predict_proba(away_input)[0][1]

    predicted_winner = home_team if home_prob > away_prob else away_team

    return {
        "sport": "soccer",
        "home_team": home_team,
        "away_team": away_team,
        "home_win_prob": round(home_prob, 3),
        "away_win_prob": round(away_prob, 3),
        "predicted_winner": predicted_winner
    }

# NBA prediction helper
def predict_nba_match(home_team: str, away_team: str):
    # Convert team names → IDs
    home_row = nba_teams_df[nba_teams_df["CITY"] + " " + nba_teams_df["NICKNAME"] == home_team]
    away_row = nba_teams_df[nba_teams_df["CITY"] + " " + nba_teams_df["NICKNAME"] == away_team]

    if home_row.empty or away_row.empty:
        raise ValueError("One or both NBA teams not found")

    home_team_id = int(home_row.iloc[0]["TEAM_ID"])
    away_team_id = int(away_row.iloc[0]["TEAM_ID"])

    home_rows = nba_features[nba_features["team"] == home_team_id]
    away_rows = nba_features[nba_features["team"] == away_team_id]

    if home_rows.empty or away_rows.empty:
        raise ValueError("Insufficient historical data for one or both teams")

    home_latest = home_rows.sort_values("date").iloc[-1]
    away_latest = away_rows.sort_values("date").iloc[-1]

    home_input = [[
        1,
        home_latest["points_for_rolling"],
        home_latest["points_against_rolling"],
        home_latest["win_rate_rolling"],
        home_latest["point_diff_rolling"]
    ]]

    away_input = [[
        0,
        away_latest["points_for_rolling"],
        away_latest["points_against_rolling"],
        away_latest["win_rate_rolling"],
        away_latest["point_diff_rolling"]
    ]]

    home_prob = nba_model.predict_proba(home_input)[0][1]
    away_prob = nba_model.predict_proba(away_input)[0][1]

    predicted_winner = home_team if home_prob > away_prob else away_team

    return {
        "sport": "nba",
        "home_team": home_team,
        "away_team": away_team,
        "home_win_prob": round(home_prob, 3),
        "away_win_prob": round(away_prob, 3),
        "predicted_winner": predicted_winner
    }

def predict_nfl_match(home_team: str, away_team: str):
    home_rows = nfl_features[nfl_features["team"] == home_team]
    away_rows = nfl_features[nfl_features["team"] == away_team]

    if home_rows.empty or away_rows.empty:
        raise ValueError("One or both NFL teams not found")

    home_latest = home_rows.sort_values("date").iloc[-1]
    away_latest = away_rows.sort_values("date").iloc[-1]

    home_input = [[
        1,
        home_latest["points_for_rolling"],
        home_latest["points_against_rolling"],
        home_latest["win_rate_rolling"],
        home_latest["point_diff_rolling"]
    ]]

    away_input = [[
        0,
        away_latest["points_for_rolling"],
        away_latest["points_against_rolling"],
        away_latest["win_rate_rolling"],
        away_latest["point_diff_rolling"]
    ]]

    home_prob = nfl_model.predict_proba(home_input)[0][1]
    away_prob = nfl_model.predict_proba(away_input)[0][1]

    return {
        "sport": "nfl",
        "home_team": home_team,
        "away_team": away_team,
        "home_win_prob": round(home_prob, 3),
        "away_win_prob": round(away_prob, 3),
        "predicted_winner": home_team if home_prob > away_prob else away_team
    }


#For soccer /teams endpoint
def get_soccer_teams():
    teams = sorted(soccer_features["team"].unique().tolist())
    return [
        {
            "id": team,
            "name": team
        }
        for team in teams
    ]

#For NBA /teams endpoint
def get_nba_teams():
    return [
        {
            "id": int(row["TEAM_ID"]),
            "name": f'{row["CITY"]} {row["NICKNAME"]}'
        }
        for _, row in nba_teams_df.iterrows()
    ]

def get_nfl_teams():
    teams = sorted(nfl_features["team"].unique().tolist())
    return [{"id": team, "name": team} for team in teams]


@app.get("/teams")
def get_teams(sport: str):
    sport = sport.lower()

    if sport == "soccer":
        return get_soccer_teams()

    elif sport == "nba":
        return get_nba_teams()
    
    elif sport == "nfl":
        return get_nfl_teams()

    else:
        return {
            "error": f"Unsupported sport: {sport}"
        }


# API route
@app.get("/predict")
def predict(
    sport: str,
    home_team: str,
    away_team: str
):
    sport = sport.lower()

    try:
        if sport == "soccer":
            return predict_soccer_match(home_team, away_team)

        elif sport == "nba":
            return predict_nba_match(home_team, away_team)
        
        elif sport == "nfl":
            return predict_nfl_match(home_team, away_team)

        else:
            return {"error": f"Unsupported sport: {sport}"}

    except ValueError as e:
        return {"error": str(e)
        }




# Health check
@app.get("/")
def root():
    return {"status": "Sports Prediction API is running"}

