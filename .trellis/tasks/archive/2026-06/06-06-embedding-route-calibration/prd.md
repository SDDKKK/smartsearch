# Embedding route calibration

## Goal

Add a repeatable calibration workflow for the optional embedding-based intent
router, then use that workflow to make semantic routing thresholds model-aware
instead of relying on one fixed cosine score.

## Requirements

- R1: Add a lightweight calibration dataset for `docs_search`, `web_search`,
  `web_fetch`, `vertical_search`, plus ordinary/ambiguous negative examples.
- R2: Add `smart-search route-calibrate` with `--models CSV` and standard
  `--format json|markdown|content` output.
- R3: Calibration output must include model availability, dimension, latency,
  semantic-only Macro-F1, full-route Macro-F1, recommended threshold/margin,
  confusion matrices, and representative failures.
- R4: Replace the hard-coded semantic confidence threshold with config-backed
  `INTENT_EMBEDDING_THRESHOLD` and `INTENT_EMBEDDING_MARGIN`.
- R5: Semantic routing may add a capability only when the top score crosses the
  threshold and its top-vs-second margin crosses the margin. Ambiguous semantic
  matches must remain signals only.
- R6: `doctor` and `route` must expose the active embedding model, threshold,
  margin, and whether threshold/margin came from defaults.
- R7: Documentation and packaged skill assets must explain that embedding
  thresholds are model-specific and should be recalibrated after model changes.

## Acceptance Criteria

- [x] `smart-search route-calibrate --format json` returns successful and failed
  model entries without aborting the whole calibration run.
- [x] `route-calibrate` can evaluate the five planned candidate models when the
  configured embedding endpoint supports them.
- [x] Semantic-only scoring uses Macro-F1 as the primary model/threshold metric.
- [x] Full-route scoring is reported as validation, not as the primary selector.
- [x] Existing `search`, `route`, `doctor`, `deep`, and provider fallback
  contracts remain capability-first and fail-open for optional remote routing.
- [x] Source validation passes: pytest, compileall, regression, mock smoke, and
  diff check.
