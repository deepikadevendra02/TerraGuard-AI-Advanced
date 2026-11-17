"""Optional Random Forest training pipeline for a REAL labelled dataset.

Do not train on the included demo_scenarios.csv. That file is synthetic and is
only for interface demonstrations. Provide a CSV with verified observations
and a binary target column `landslide` (1=event, 0=non-event).
"""
import argparse
import json
from pathlib import Path

FEATURES = [
    "rain_1h_mm", "rain_24h_mm", "rain_72h_mm", "slope_deg",
    "soil_moisture_pct", "landcover_disturbance", "geology_susceptibility",
    "drainage_impairment", "past_landslide"
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to verified labelled CSV")
    parser.add_argument("--out", default="models/landslide_rf.joblib")
    args = parser.parse_args()
    try:
        import pandas as pd
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.impute import SimpleImputer
        from sklearn.pipeline import Pipeline
        from sklearn.metrics import classification_report, roc_auc_score
        from sklearn.model_selection import GroupShuffleSplit, train_test_split
        import joblib
    except ImportError as exc:
        raise SystemExit("Install optional ML packages: pip install -r requirements-ml.txt") from exc

    df = pd.read_csv(args.csv)
    missing = [c for c in FEATURES + ["landslide"] if c not in df.columns]
    if missing:
        raise SystemExit(f"CSV is missing columns: {missing}")
    if df["landslide"].nunique() != 2:
        raise SystemExit("The target column must contain both 0 (non-landslide) and 1 (landslide).")
    X, y = df[FEATURES], df["landslide"].astype(int)
    # Prefer grouped split when a region/site group is provided to reduce spatial leakage.
    if "region_id" in df.columns and df["region_id"].nunique() >= 2:
        splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
        train_idx, test_idx = next(splitter.split(X, y, groups=df["region_id"]))
        X_train, X_test, y_train, y_test = X.iloc[train_idx], X.iloc[test_idx], y.iloc[train_idx], y.iloc[test_idx]
        split_note = "region-group holdout"
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y
        )
        split_note = "random stratified holdout; spatial leakage may remain"
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("forest", RandomForestClassifier(
            n_estimators=400, min_samples_leaf=3, class_weight="balanced",
            random_state=42, n_jobs=-1
        ))
    ])
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]
    print("Split:", split_note)
    print(classification_report(y_test, pred, zero_division=0))
    if y_test.nunique() == 2:
        print("ROC-AUC:", round(roc_auc_score(y_test, prob), 4))
    else:
        print("ROC-AUC unavailable: test split has only one class.")
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES, "split_note": split_note}, out)
    print("Saved model:", out)

if __name__ == "__main__":
    main()
