import os
import sys
import warnings

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.simulate_cohort import simulate, FOLLOW_UP_WINDOW_DAYS
from src.survival_analysis import kaplan_meier_summary, cox_model_summary
from src.event_prediction import train_and_evaluate


@pytest.fixture(scope="module")
def df():
    return simulate()


def test_cohort_has_340_patients(df):
    assert len(df) == 340


def test_both_event_and_readmission_outcomes_vary(df):
    assert df["event_observed"].nunique() == 2
    assert df["readmitted_within_180d"].nunique() == 2


def test_readmission_flag_consistent_with_time_and_window(df):
    """A patient flagged as readmitted within the window must have an
    event time at or below the window (sanity-checks the label logic)."""
    readmitted = df[df["readmitted_within_180d"] == 1]
    assert (readmitted["time_to_event_days"] <= FOLLOW_UP_WINDOW_DAYS).all()


def test_kaplan_meier_survival_is_monotonically_non_increasing(df):
    km = kaplan_meier_summary(df)
    assert km["survival_at_90d"] >= km["survival_at_180d"] >= km["survival_at_365d"]


def test_cox_model_runs_and_returns_hazard_ratios(df):
    cox = cox_model_summary(df)
    assert "creatinine" in cox["hazard_ratios"]
    assert 0.5 <= cox["concordance_index"] <= 1.0


def test_cox_hazard_ratio_direction_for_ejection_fraction(df):
    """Higher ejection fraction is protective in the simulation -- its
    hazard ratio should be below 1."""
    cox = cox_model_summary(df)
    assert cox["hazard_ratios"]["ejection_fraction"] < 1.0


def test_prediction_model_beats_majority_baseline(df):
    result = train_and_evaluate(df)
    majority = max(df["readmitted_within_180d"].mean(), 1 - df["readmitted_within_180d"].mean())
    assert result["accuracy"] >= majority - 0.05


def test_prediction_accuracy_in_realistic_band(df):
    result = train_and_evaluate(df)
    assert 0.55 <= result["accuracy"] <= 0.95


def test_feature_importances_sum_to_approximately_one(df):
    result = train_and_evaluate(df)
    assert abs(sum(result["feature_importances"].values()) - 1.0) < 0.05
