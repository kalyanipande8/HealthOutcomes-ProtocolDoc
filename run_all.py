"""End-to-end: simulate the 340-patient longitudinal cohort, run Kaplan-
Meier + Cox survival analysis, and evaluate the 180-day readmission
prediction model."""
import json
import os

from src.simulate_cohort import simulate, FOLLOW_UP_WINDOW_DAYS
from src.survival_analysis import kaplan_meier_summary, cox_model_summary
from src.event_prediction import train_and_evaluate

os.makedirs("data", exist_ok=True)
os.makedirs("results", exist_ok=True)

print("=== Simulating 340-patient longitudinal heart-failure cohort ===")
df = simulate()
df.to_csv("data/cohort.csv", index=False)
print(df.shape)
print(f"Event rate: {df['event_observed'].mean():.3f}, "
      f"{FOLLOW_UP_WINDOW_DAYS}-day readmission rate: {df['readmitted_within_180d'].mean():.3f}")

print("\n=== Kaplan-Meier survival estimation ===")
km = kaplan_meier_summary(df)
print(km)

print("\n=== Cox Proportional Hazards regression ===")
cox = cox_model_summary(df)
print(cox)

print(f"\n=== {FOLLOW_UP_WINDOW_DAYS}-day readmission prediction (RandomForest) ===")
prediction = train_and_evaluate(df)
print(prediction)

summary = {
    "n_patients": len(df),
    "event_rate": round(float(df["event_observed"].mean()), 4),
    "readmission_rate_180d": round(float(df["readmitted_within_180d"].mean()), 4),
    "km_median_survival_days": km["median_survival_days"],
    "km_survival_at_180d": km["survival_at_180d"],
    "cox_concordance_index": cox["concordance_index"],
    "prediction_accuracy": prediction["accuracy"],
    "prediction_auc": prediction["auc"],
}
with open("results/summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)

print("\n=== Summary ===")
print(json.dumps(summary, indent=2, default=str))
