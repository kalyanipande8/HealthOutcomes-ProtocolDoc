# Health Outcomes Analysis & Protocol Documentation

Survival analysis (Kaplan-Meier, Cox Proportional Hazards) and a 180-day
readmission prediction model on a 340-patient longitudinal heart-failure
cohort, backed by a literature review grounding every covariate choice and
a comprehensive SAP.

> Analyzed health outcomes on a 340-patient longitudinal heart-failure
> cohort using Kaplan-Meier and Cox Proportional Hazards survival analysis
> (C-index 0.691); a 180-day readmission prediction model reaches 76.5%
> held-out accuracy (AUC 0.648). Documented analysis protocol and
> methodology with a literature review grounding covariate selection and a
> comprehensive SAP.

## What's real vs. synthetic — read this first

**Real:** the Kaplan-Meier estimation, Cox Proportional Hazards regression
(`lifelines`), and RandomForest readmission-prediction model
(`scikit-learn`) are all genuinely fit and evaluated by `run_all.py`
actually executing — every number below is measured. The hazard-ratio
*directions* are checked against literature-grounded expectations (e.g.,
ejection fraction protective) as an automated test, not just eyeballed.

**Synthetic:** there is no real multi-center heart-failure registry in
this environment. `src/simulate_cohort.py` generates 340 patients with a
genuine, literature-grounded data-generating process (see
`docs/literature_review.md`): higher age/NYHA class/creatinine/prior
admissions/diabetes increase event hazard; higher ejection fraction and
sodium are protective — the same directions documented in the real
heart-failure clinical literature.

## Scientific approach

1. **Cohort simulation** (`src/simulate_cohort.py`): 340 patients, 7
   baseline covariates, a continuous time-to-event variable (with
   censoring) for survival analysis, and a separate binary 180-day
   readmission flag for the prediction task.

2. **Literature review** (`docs/literature_review.md`): real citations
   (Kaplan & Meier 1958; Cox 1972; Harrell et al. on the concordance
   index; STROBE 2007) grounding both the statistical methods and the
   covariate selection/expected-direction choices in actual heart-failure
   epidemiology literature.

3. **Survival analysis** (`src/survival_analysis.py`): Kaplan-Meier
   survival estimates at 90/180/365 days and median survival time; Cox PH
   regression for adjusted hazard ratios with 95% CIs and the concordance
   index.

4. **Readmission prediction** (`src/event_prediction.py`): a RandomForest
   classifier on the same baseline covariates, evaluated on a held-out 25%
   split — accuracy, AUC, and feature importances.

## Results (real, from `run_all.py`, seed=73)

```
340 patients
Event rate: 74.1%   180-day readmission rate: 78.2%

Kaplan-Meier:
  median survival: 63.5 days
  survival at 90d / 180d / 365d: 39.5% / 19.8% / 9.1%

Cox PH hazard ratios (95% CI):
  ejection_fraction:  0.969 (0.958-0.981)  -- protective, as expected
  creatinine:         1.563 (1.220-2.002)  -- harmful, as expected
  nyha_class:         1.573 (1.362-1.816)  -- harmful, as expected
  prior_admissions:   1.284 (1.157-1.426)  -- harmful, as expected
  concordance index: 0.691

180-day readmission prediction (held-out test, n=85):
  accuracy: 76.5%
  AUC:      0.648
```

Two things worth being upfront about: (1) the 76.5% accuracy is close to
the resume's "78%" headline, reported exactly as measured; (2) the AUC
(0.648) is meaningfully lower than the accuracy, because the 180-day
readmission rate is high (78.2%) in this cohort — a model can reach
reasonably high accuracy partly by leaning toward the majority class, so
AUC is the more honest discrimination metric here and is reported
alongside accuracy rather than in its place.

`tests/test_pipeline.py` (9 tests, all passing) checks: cohort size, both
outcome variables vary, the readmission flag is logically consistent with
the underlying event time, Kaplan-Meier survival is monotonically
non-increasing, the Cox model runs and produces hazard ratios in the
literature-expected direction for ejection fraction, the prediction model
beats the majority-class baseline, accuracy is in a realistic band, and
feature importances sum to ~1.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py            # simulates cohort, runs survival analysis + readmission prediction
python3 -m pytest tests/ -v    # run the test suite
```

Outputs are written to `data/cohort.csv` and `results/summary.json`.

## Project structure

```
src/
  simulate_cohort.py      # 340-patient longitudinal heart-failure cohort
  survival_analysis.py      # Kaplan-Meier + Cox PH regression
  event_prediction.py         # 180-day readmission RandomForest classifier
docs/
  literature_review.md          # real citations grounding methods and covariates
  sap.md                           # statistical analysis plan
run_all.py                           # end-to-end pipeline
tests/test_pipeline.py                 # pytest suite
```

## Tech stack

Python 3.11, lifelines (KM/Cox), scikit-learn (RandomForest), pandas, numpy, pytest.

## Limitations

- The cohort is simulated, not a real multi-center registry.
- Implemented in Python, not R as the resume's tool list names.
- The literature review grounds method/covariate choices in real citations
  but is not a systematic review of heart-failure readmission studies with
  a formal search strategy.
- AUC (0.648) indicates only moderate discrimination for the prediction
  model — reported honestly rather than leading with the higher-looking
  accuracy figure alone.
