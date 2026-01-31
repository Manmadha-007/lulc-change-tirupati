import pandas as pd
import joblib
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from config import PROCESSED_DIR, RANDOM_FOREST_PARAMS


def train_rf():
    # =========================
    # Paths
    # =========================
    data_path = PROCESSED_DIR / "training" / "training_pixels_2018.csv"
    model_dir = Path("data/models")
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / "rf_lulc_model.pkl"
    metrics_path = model_dir / "rf_metrics.txt"

    # =========================
    # Load data
    # =========================
    print("Loading training data...")
    df = pd.read_csv(data_path)

    # =========================
    # MEMORY SAFETY: Subsample
    # =========================
    MAX_SAMPLES = 250_000  # safe for laptops, sufficient for LULC

    if len(df) > MAX_SAMPLES:
        df = df.sample(n=MAX_SAMPLES, random_state=42)
        print(f"Subsampled training data to {MAX_SAMPLES} pixels")

    # =========================
    # Features & labels
    # =========================
    X = df[["blue", "green", "red", "nir", "ndvi"]]
    y = df["label"]

    # =========================
    # Train / validation split
    # =========================
    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # =========================
    # Train model
    # =========================
    print("Training Random Forest...")
    rf = RandomForestClassifier(**RANDOM_FOREST_PARAMS)
    rf.fit(X_train, y_train)

    # =========================
    # Evaluation
    # =========================
    print("Evaluating model...")
    y_pred = rf.predict(X_val)

    report = classification_report(y_val, y_pred, digits=3)
    cm = confusion_matrix(y_val, y_pred)

    print(report)
    print("Confusion Matrix:\n", cm)

    # =========================
    # Save outputs
    # =========================
    joblib.dump(rf, model_path)

    with open(metrics_path, "w") as f:
        f.write("Classification Report:\n")
        f.write(report)
        f.write("\n\nConfusion Matrix:\n")
        f.write(str(cm))

    print("\nModel saved to:", model_path)
    print("Metrics saved to:", metrics_path)


if __name__ == "__main__":
    train_rf()
