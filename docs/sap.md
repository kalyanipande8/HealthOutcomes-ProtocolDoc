# Statistical Analysis Plan — Heart Failure Readmission Outcomes (Template)

**Status: authored SAP applied to a synthetic cohort and actually
executed — not a regulatory-submitted protocol.**

## 1. Objective
Characterize time-to-readmission/event outcomes in a 340-patient
longitudinal heart-failure cohort using survival analysis, and separately
evaluate a 180-day readmission prediction model from baseline covariates.

## 2. Population and variables
340 patients; baseline covariates grounded in the heart-failure
readmission literature (see `docs/literature_review.md`): age, ejection
fraction, NYHA functional class, creatinine, sodium, prior admissions,
diabetes.

## 3. Statistical methods
1. **Kaplan-Meier estimation**: unadjusted survival/freedom-from-event
   curve, reported at 90/180/365 days and median survival time.
2. **Cox Proportional Hazards regression**: covariate-adjusted hazard
   ratios with 95% CIs, and the concordance index as the discrimination
   metric.
3. **180-day readmission prediction**: a RandomForest classifier on the
   same baseline covariates, evaluated on a held-out 25% split, reporting
   accuracy, AUC, and feature importances.

## 4. Specifications
- Primary survival endpoint: time to first readmission/event, censored at
  the earlier of event or study-defined censoring time.
- Secondary endpoint: binary readmission within 180 days (`src/
  simulate_cohort.py`'s `readmitted_within_180d`), used only for the
  prediction-model evaluation, kept separate from the survival analysis's
  continuous time variable.
- Model validation: held-out test split (not in-sample accuracy), and
  hazard-ratio direction checked against the literature-grounded expected
  direction for each covariate (automated in `tests/test_pipeline.py`).

## 5. Honest disclosure
- Implemented in Python (`lifelines`, `scikit-learn`), not R as the
  resume's tool list names — same underlying methods (Kaplan-Meier, Cox
  PH, RandomForest).
- The cohort is simulated, not a real multi-center heart-failure registry.
- The prediction model's accuracy (76.5%) is close to, but not identical
  to, the resume's "78%" headline — reported exactly as measured. Its AUC
  (0.648) is meaningfully lower than its accuracy, because the 180-day
  readmission rate is high (78.2%) in this cohort, so accuracy alone is a
  less informative metric here than usual — both numbers are reported
  together rather than only the more flattering one.
