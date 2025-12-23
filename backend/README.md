# 🏆 International Football Match Prediction Pipeline

An end-to-end machine learning project that predicts the outcome of international football matches using historical data, rolling performance features, and supervised learning models.  
The project demonstrates a full **data → model → API** pipeline using Python, pandas, scikit-learn, and FastAPI.

---

## 📌 Project Overview

This project builds a production-style machine learning workflow that:

- Ingests raw historical football match data
- Cleans and preprocesses the data
- Engineers rolling performance features at the team level
- Trains and evaluates machine learning models
- Combines team-level predictions into match-level predictions
- Serves predictions through a REST API

The dataset includes **45,000+ international matches** spanning multiple decades.

---

## 🔄 Data Pipeline

### 1️⃣ Load Data
- Reads raw CSV match data using pandas
- Inspects schema, data types, and missing values

### 2️⃣ Clean Data
- Standardizes column formats
- Converts dates to datetime
- Derives match outcomes (`home_win`, `away_win`, `draw`)
- Removes invalid or incomplete records

### 3️⃣ Feature Engineering
- Converts match-level data into team-level observations
- Creates rolling statistics per team:
  - Rolling goals scored
  - Rolling goals conceded
  - Rolling win rate
- Encodes home/away context explicitly

These rolling features allow the model to learn **form and momentum**, not just raw scores.

---

## 🤖 Machine Learning Models

Two models are trained and compared:

### Logistic Regression (Baseline)
- Simple, interpretable linear classifier
- Serves as a strong baseline

### Random Forest Classifier
- Non-linear ensemble model
- Captures interactions and thresholds between features

Both models are trained using the same feature set and evaluated on a held-out test set.

---

## 📊 Model Evaluation

Metrics used:
- Accuracy
- Baseline comparison (home-only prediction)
- Match-level accuracy after combining team predictions

### Example Results
- Logistic Regression Accuracy: **~73.6%**
- Random Forest Accuracy: **~73.6%**
- Match-Level Accuracy: **~65%**

---

## 🔁 Match-Level Prediction Logic

Instead of predicting matches directly, the system:
1. Predicts **win probability for each team**
2. Combines home and away probabilities
3. Selects the team with the higher probability as the predicted winner

This mirrors how real sports analytics systems operate.

---

## 🌐 API Deployment (FastAPI)

The trained Random Forest model is deployed via a REST API.

### Start the API
```bash
uvicorn src.api:app --reload
```

### Interactive Docs
```bash
http://127.0.0.1:8000/docs
```

### Example Request
```bash
/predict?home_team=Brazil&away_team=Germany
```

### Example Response
```bash
{
  "home_team": "Brazil",
  "away_team": "Germany",
  "home_win_prob": 0.62,
  "away_win_prob": 0.38,
  "predicted_winner": "Brazil"
}
```

## ⚖️ Model Comparison: Logistic Regression vs Random Forest

### Why Both Models Were Used

Using two different models allows us to evaluate:

- Predictive performance  
- Interpretability  
- Model complexity trade-offs  

---

### Logistic Regression

#### Advantages
- Highly interpretable coefficients  
- Fast to train and predict  
- Less prone to overfitting on small feature sets  
- Easy to explain in production environments  

#### Disadvantages
- Assumes linear decision boundaries  
- Cannot naturally capture feature interactions  
- Limited flexibility with complex patterns  

---

### Random Forest

#### Advantages
- Captures non-linear relationships  
- Handles feature interactions automatically  
- Robust to outliers and noise  
- Provides feature importance scores  

#### Disadvantages
- Less interpretable than linear models  
- More computationally expensive  
- Gains are limited if features are already well-engineered  

---

### Why Both Achieved Similar Accuracy

Both models achieved nearly identical accuracy because the engineered rolling features produce an **approximately linear decision boundary**.  
With strong, smooth features (win rate, goal averages, and home advantage), logistic regression is already close to optimal.

In this scenario:
- **Logistic Regression** excels due to simplicity  
- **Random Forest** confirms feature importance but offers limited additional lift  
