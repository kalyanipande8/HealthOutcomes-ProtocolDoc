"""Predicts whether a patient is readmitted within the 180-day follow-up
window from baseline covariates -- a classification task distinct from
(but complementary to) the survival analysis above, evaluated with a
held-out train/test split."""
from __future__ import annotations

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

from .survival_analysis import COVARIATES

SEED = 73


def train_and_evaluate(df, seed: int = SEED) -> dict:
    X = df[COVARIATES].values
    y = df["readmitted_within_180d"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=seed, stratify=y)
    clf = RandomForestClassifier(n_estimators=300, max_depth=5, random_state=seed)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    probs = clf.predict_proba(X_test)[:, 1]

    return {
        "accuracy": round(float(accuracy_score(y_test, preds)), 4),
        "auc": round(float(roc_auc_score(y_test, probs)), 4),
        "n_train": len(X_train), "n_test": len(X_test),
        "feature_importances": dict(zip(COVARIATES, [round(float(x), 4) for x in clf.feature_importances_])),
    }


if __name__ == "__main__":
    from .simulate_cohort import simulate

    df = simulate()
    print(train_and_evaluate(df))
