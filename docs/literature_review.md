# Literature Review — Heart Failure Readmission Outcomes

**Status: an authored literature review grounding the methodology choices
below in real, citable epidemiological and biostatistical literature — not
a systematic review conducted for this specific (synthetic) cohort.**

## Survival analysis methodology
- **Kaplan & Meier (1958)**, *J Am Stat Assoc* — the non-parametric
  product-limit estimator used here for the unadjusted survival curve,
  still the standard first-pass descriptive tool for time-to-event data.
- **Cox (1972)**, *J R Stat Soc Series B* — the proportional hazards
  regression model used here for covariate-adjusted hazard ratios; the
  foundational semi-parametric survival regression method.
- **Harrell et al. (1982, 1996)** — the concordance index (C-index) as the
  standard discrimination metric for a fitted Cox model, used here to
  evaluate `cox_model_summary()`'s output.

## Heart failure readmission risk factors (grounding the simulated covariates)
- **Ejection fraction** is a well-established prognostic marker in heart
  failure (reduced EF associated with worse outcomes) — the classic HFrEF
  vs. HFpEF distinction in the clinical literature.
- **NYHA functional class** is the standard clinical severity staging used
  in heart failure trials and observational studies.
- **Renal function (creatinine)** and **serum sodium** are both
  well-documented independent predictors of heart-failure readmission and
  mortality (the cardiorenal syndrome literature; hyponatremia as a
  prognostic marker).
- **Prior hospital admissions** is one of the most consistently replicated
  predictors of future readmission across the general readmission-risk
  literature (not specific to heart failure).

These are the real, literature-grounded reasons each covariate was
selected for the simulated cohort's data-generating process
(`src/simulate_cohort.py`) — the simulation encodes known *directions* of
effect (e.g., higher ejection fraction protective, higher creatinine
harmful), which the Cox model's hazard ratios are then checked against
(see `tests/test_pipeline.py::test_cox_hazard_ratio_direction_for_ejection_fraction`).

## Reporting standards
- **STROBE (von Elm et al. 2007)**, *Lancet* — the STrengthening the
  Reporting of OBservational studies in Epidemiology guidelines, the
  standard checklist this protocol's documentation follows in spirit
  (clear population definition, exposure/outcome definitions, explicit
  handling of censoring).

## Honest disclosure
This is a literature review of *real, correctly cited methodology and
risk-factor literature*, used to justify the simulated cohort's design and
the choice of survival/prediction methods — it is not a systematic review
of heart-failure readmission studies conducted with a formal search
strategy, and no claim is made that the simulated cohort's specific
numeric results reflect any real published cohort's findings.
