# 🏆 Sports Match Predictor Platform

> A full-stack machine learning web application that predicts outcomes of international soccer, NBA, and NFL games using statistical modeling, real historical datasets, and cloud-deployed APIs.

---

# 🌐 Live Demo

## 🚀 Frontend (Vercel)
https://sports-prediction-platform.vercel.app

## ⚡ Backend API (Render)
https://sports-prediction-platform.onrender.com

---

# 📸 Preview

## 🏠 Home Dashboard
- Multi-sport landing page
- Interactive sport cards
- Dynamic navigation

## ⚽ Soccer Predictor
- International match predictions
- Country flags + win probabilities
- Match breakdown visualization

## 🏀 NBA Predictor
- NBA team logo rendering
- Real-time prediction API
- Probability comparison UI

## 🏈 NFL Predictor
- Full NFL team support
- Dynamic logo loading
- ML-powered matchup predictions

---

# ✨ Features

## 🧠 Machine Learning Predictions
- Separate ML models for:
  - Soccer
  - NBA
  - NFL
- Historical statistical analysis
- Rolling performance feature engineering
- Real-time inference through REST APIs

---

## ⚙️ Full-Stack Architecture

### Frontend
- React
- React Router
- Responsive UI
- Dynamic rendering
- Team logos & assets
- Probability visualizations

### Backend
- FastAPI
- REST API architecture
- Model loading at runtime
- CORS-enabled production APIs

### Machine Learning
- scikit-learn
- Pandas
- Logistic Regression
- Rolling statistical features

---

# 🏗️ System Architecture

```text
                ┌────────────────────┐
                │    React Frontend   │
                │      (Vercel)       │
                └─────────┬──────────┘
                          │ HTTPS Requests
                          ▼
                ┌────────────────────┐
                │   FastAPI Backend   │
                │      (Render)       │
                └─────────┬──────────┘
                          │
          ┌───────────────┼────────────────┐
          ▼               ▼                ▼
   Soccer Model      NBA Model       NFL Model
  (scikit-learn)   (scikit-learn)  (scikit-learn)
```

---

# 📊 Machine Learning Pipeline

## Feature Engineering
Custom rolling statistical features were engineered for each sport, including:

- Win rate trends
- Offensive performance
- Defensive performance
- Point / goal differentials
- Home vs away context

---

## NFL Pipeline Example

```python
points_for_rolling
points_against_rolling
win_rate_rolling
point_diff_rolling
```

The resulting dataset was used to train classification models capable of predicting likely winners.

---

# 🧪 Model Performance

| Sport | Model Type | Accuracy |
|------|------------|----------|
| Soccer | Classification Model | Real-time inference |
| NBA | Classification Model | Real-time inference |
| NFL | Logistic Regression | ~72% accuracy |

---

# 🗂️ Project Structure

```text
sports-prediction-platform/
│
├── frontend/
│   ├── public/
│   │   ├── nba_logos/
│   │   ├── nfl_logos/
│   │   ├── soccer flags
│   │   ├── nba-bg.jpg
│   │   ├── nfl-bg.png
│   │   └── soccer-bg.jpg
│   │
│   └── src/
│       ├── components/
│       │   ├── SoccerPredictor.js
│       │   ├── NbaPredictor.js
│       │   └── NflPredictor.js
│       │
│       └── pages/
│           ├── SoccerPage.js
│           ├── NbaPage.js
│           └── NflPage.js
│
├── backend/
│   ├── src/
│   │   ├── api.py
│   │   ├── soccer/
│   │   ├── nba/
│   │   └── nfl/
│   │
│   ├── models/
│   │   ├── soccer_model.pkl
│   │   ├── nba_model.pkl
│   │   └── nfl_model.pkl
│   │
│   └── data/
│       ├── soccer/
│       ├── nba/
│       └── nfl/
│
└── README.md
```

---

# 🚀 Deployment

## Frontend
Deployed using:
- Vercel
- Global CDN delivery
- Environment-based API configuration

## Backend
Deployed using:
- Render
- FastAPI + Uvicorn
- Cloud-hosted ML inference

---

# 🔥 Engineering Challenges Solved

## ✅ Cross-Origin Resource Sharing (CORS)
Configured FastAPI middleware to securely enable communication between:
- Vercel frontend
- Render backend

---

## ✅ Production Deployment
Handled:
- Environment configuration
- API routing
- Asset serving
- Cloud deployment debugging

---

## ✅ Dynamic Asset Rendering
Implemented dynamic loading of:
- NBA logos
- NFL logos
- Soccer flags
- Fallback rendering logic

---

# 💡 Future Improvements

- Live sports API integration
- User authentication
- Prediction history tracking
- Betting line comparison
- Advanced ML models (XGBoost, Neural Networks)
- Real-time game updates

---

# 🛠️ Technologies Used

## Frontend
- React
- React Router
- CSS3
- JavaScript

## Backend
- Python
- FastAPI
- Uvicorn

## Machine Learning / Data
- scikit-learn
- Pandas
- NumPy
- Joblib

## Deployment
- Vercel
- Render
- GitHub

---

# 📈 Resume Highlights

- Designed and deployed a full-stack sports prediction platform supporting Soccer, NBA, and NFL game outcome predictions.
- Engineered machine-learning pipelines with rolling statistical feature generation and trained classification models using historical sports datasets.
- Built cloud-hosted FastAPI APIs serving real-time predictions to a React frontend deployed on Vercel.
- Implemented responsive UI components with dynamic team rendering, probability visualizations, and production-ready API integration.

---

# 👨‍💻 Author

**Will Piwow**  
Computer Science @ University of Pittsburgh

---

# ⭐ Final Note

This project demonstrates:
- End-to-end full-stack engineering
- Production deployment
- Machine learning integration
- REST API architecture
- Real-world debugging and deployment workflows

It was built to simulate the architecture and engineering practices used in modern production web applications.
