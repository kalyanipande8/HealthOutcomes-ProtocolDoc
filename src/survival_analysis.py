"""Kaplan-Meier estimation and Cox Proportional Hazards regression for the
heart-failure readmission cohort -- the core epidemiological survival
methods (Kaplan & Meier 1958; Cox 1972)."""
from __future__ import annotations

import numpy as np
from lifelines import KaplanMeierFitter, CoxPHFitter

COVARIATES = ["age", "ejection_fraction", "nyha_class", "creatinine", "sodium", "prior_admissions", "diabetes"]


def kaplan_meier_summary(df) -> dict:
    kmf = KaplanMeierFitter()
    kmf.fit(df["time_to_event_days"], df["event_observed"])
    return {
        "median_survival_days": kmf.median_survival_time_,
        "survival_at_90d": round(float(kmf.survival_function_at_times(90).iloc[0]), 4),
        "survival_at_180d": round(float(kmf.survival_function_at_times(180).iloc[0]), 4),
        "survival_at_365d": round(float(kmf.survival_function_at_times(365).iloc[0]), 4),
    }


def cox_model_summary(df) -> dict:
    cph = CoxPHFitter(penalizer=0.1)
    cols = COVARIATES + ["time_to_event_days", "event_observed"]
    cph.fit(df[cols], duration_col="time_to_event_days", event_col="event_observed")

    hazard_ratios = cph.hazard_ratios_.round(4).to_dict()
    ci = np.exp(cph.confidence_intervals_)
    ci_dict = {cov: [round(float(ci.loc[cov].iloc[0]), 4), round(float(ci.loc[cov].iloc[1]), 4)] for cov in COVARIATES}

    return {
        "hazard_ratios": hazard_ratios,
        "hazard_ratio_95ci": ci_dict,
        "concordance_index": round(float(cph.concordance_index_), 4),
    }


if __name__ == "__main__":
    from .simulate_cohort import simulate

    df = simulate()
    print(kaplan_meier_summary(df))
    print(cox_model_summary(df))
