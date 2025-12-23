# Sports Match Prediction API

A FastAPI-based machine learning backend that predicts match outcomes for **Soccer** and **NBA** games using historical data, feature engineering, and trained classification models.

---

## 🚀 Features

- Supports **multiple sports** (Soccer & NBA)
- Machine learning predictions using:
  - Logistic Regression
  - Random Forest
- Rolling feature engineering (recent performance trends)
- Match-level probability predictions
- REST API built with **FastAPI**
- Designed for easy frontend integration

---

## 🧠 How Predictions Work

Instead of predicting match results directly, the system:

1. Builds **team-level rolling statistics** (recent wins, scoring, defense)
2. Predicts **win probability for each team**
3. Compares probabilities
4. Returns the team with the higher probability as the predicted winner

This mirrors real-world sports analytics systems.

---

## 📂 Project Structure

backend/
├── src/
│ ├── api.py # FastAPI app + endpoints
│ ├── soccer/ # Soccer pipeline (ingest, features, models)
│ └── nba/ # NBA pipeline (ingest, features, models)
├── data/
│ ├── soccer/
│ └── nba/
├── models/
│ ├── soccer/
│ └── nba/
├── requirements.txt
└── README.md


---

## 🔌 API Endpoints

### Health Check

GET/

Returns API status.

---

### Get Teams

GET /teams?sport=soccer
GET /teams?sport=nba


Returns a list of available teams for the selected sport.

---

### Predict Match

GET /predict?sport=soccer&home_team=Brazil&away_team=Germany
GET /predict?sport=nba&home_team=1610612738&away_team=1610612747


#### Example Response
```json
{
  "sport": "soccer",
  "home_team": "Brazil",
  "away_team": "Germany",
  "home_win_prob": 0.62,
  "away_win_prob": 0.38,
  "predicted_winner": "Brazil"
}
```
---

## Models Used

### Logistic Regression

* Interpretable
* Fast
* Strong baseline

### Random Forest

* Captures non-linear patterns
* Feature importance analysis
* Robust to noise

---

## Running the Backend

## Activate Virtual Environment
```bash
{
source .venv/bin/activate     # macOS/Linux
.venv\Scripts\activate        # Windows
}
```

## Install Dependencies
```bash
{
pip install -r requirements.txt
}
```

## Start API Server
```bash
{
uvicorn src.api:app --reload
}
```

## Open API Docs
```bash
{
http://127.0.0.1:8000/docs
}
```

## Notes

* Raw datasets are ignored via .gitignore
* Trained models are stored as .pkl files
* Designed to scale to additional sports (NFL, MLB)
