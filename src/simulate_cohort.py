"""Simulate a 340-patient longitudinal cohort (heart-failure readmission
context) for health outcomes analysis: time-to-event data for survival
analysis, plus baseline covariates for a separate event-within-window
prediction task."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_PATIENTS = 340
SEED = 73
FOLLOW_UP_WINDOW_DAYS = 180


def simulate(n: int = N_PATIENTS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    age = rng.normal(68, 12, n).clip(35, 95)
    ejection_fraction = rng.normal(38, 12, n).clip(10, 70)
    nyha_class = rng.choice([1, 2, 3, 4], n, p=[0.1, 0.35, 0.4, 0.15])
    creatinine = rng.normal(1.3, 0.5, n).clip(0.4, 5.0)
    sodium = rng.normal(138, 4, n).clip(120, 150)
    prior_admissions = rng.poisson(1.2, n).clip(0, 8)
    diabetes = rng.binomial(1, 0.35, n)

    # linear predictor for readmission/event hazard
    linear_pred = (
        0.03 * (age - 68)
        - 0.04 * (ejection_fraction - 38)
        + 0.5 * (nyha_class - 2)
        + 0.6 * (creatinine - 1.3)
        - 0.05 * (sodium - 138)
        + 0.25 * prior_admissions
        + 0.3 * diabetes
    )
    baseline_scale = 220.0
    u = rng.uniform(0, 1, n)
    event_time = baseline_scale * (-np.log(u)) * np.exp(-linear_pred)
    censor_time = rng.uniform(30, 365, n)
    time = np.minimum(event_time, censor_time)
    event = (event_time <= censor_time).astype(int)
    event_within_window = ((event_time <= FOLLOW_UP_WINDOW_DAYS)).astype(int)

    return pd.DataFrame({
        "patient_id": [f"HF-{i:04d}" for i in range(n)],
        "age": np.round(age, 1), "ejection_fraction": np.round(ejection_fraction, 1),
        "nyha_class": nyha_class, "creatinine": np.round(creatinine, 2),
        "sodium": np.round(sodium, 1), "prior_admissions": prior_admissions, "diabetes": diabetes,
        "time_to_event_days": np.round(time, 1), "event_observed": event,
        "readmitted_within_180d": event_within_window,
    })


if __name__ == "__main__":
    df = simulate()
    print(df.shape)
    print("Event rate:", df["event_observed"].mean())
    print("180-day readmission rate:", df["readmitted_within_180d"].mean())
