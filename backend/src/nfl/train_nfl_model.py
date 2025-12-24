import os
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


DATA_PATH = os.path.join(
    "backend", "data", "nfl", "processed", "team_games.csv"
)

MODEL_DIR = os.path.join("backend", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "nfl_model.pkl")


def train_nfl_model():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Could not find processed NFL data at:\n  {DATA_PATH}\n\n"
            f"Run build_nfl_features.py first."
        )

    os.makedirs(MODEL_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    # --- Features & target ---
    features = [
        "is_home",
        "points_for_rolling",
        "points_against_rolling",
        "win_rate_rolling",
        "point_diff_rolling"
    ]

    X = df[features]
    y = df["win"]

    # --- Train / test split ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # --- Model ---
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # --- Evaluation ---
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)

    print("✅ NFL model trained")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Train size: {len(X_train):,}")
    print(f"Test size:  {len(X_test):,}")

    # --- Save model ---
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_nfl_model()
