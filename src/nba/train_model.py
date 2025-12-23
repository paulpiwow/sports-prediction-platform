import pandas as pd
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Paths
BASE_DIR = Path(__file__).resolve().parents[2]

FEATURE_PATH = BASE_DIR / "data" / "nba" / "processed" / "team_features.csv"
MODEL_DIR = BASE_DIR / "models" / "nba"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

LR_MODEL_PATH = MODEL_DIR / "logreg_model.pkl"
RF_MODEL_PATH = MODEL_DIR / "rf_model.pkl"

# Load data
df = pd.read_csv(FEATURE_PATH)
df["date"] = pd.to_datetime(df["date"])

features = [
    "is_home",
    "points_for_rolling",
    "points_against_rolling",
    "win_rate_rolling",
    "point_diff_rolling",
]

X = df[features]
y = df["win"]

# Time-based train/test split
split_date = df["date"].quantile(0.8)

train_idx = df["date"] <= split_date
test_idx = df["date"] > split_date

X_train, X_test = X[train_idx], X[test_idx]
y_train, y_test = y[train_idx], y[test_idx]

print(f"Training rows: {len(X_train)}")
print(f"Testing rows: {len(X_test)}")

# Logistic Regression
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)

lr_preds = lr_model.predict(X_test)
lr_accuracy = accuracy_score(y_test, lr_preds)

print("\nLogistic Regression accuracy:", round(lr_accuracy, 3))

# Save Logistic Regression model
joblib.dump(lr_model, LR_MODEL_PATH)

# Random Forest
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_preds = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_preds)

print("Random Forest accuracy:", round(rf_accuracy, 3))

# Save Random Forest model
joblib.dump(rf_model, RF_MODEL_PATH)

# Feature importance (RF)
importances = pd.Series(
    rf_model.feature_importances_,
    index=features
).sort_values(ascending=False)

print("\nRandom Forest feature importance:")
print(importances)

# Summary
print("\nModel comparison:")
print(f"Logistic Regression accuracy: {round(lr_accuracy, 3)}")
print(f"Random Forest accuracy: {round(rf_accuracy, 3)}")

print("\nModels saved to:")
print(MODEL_DIR)
