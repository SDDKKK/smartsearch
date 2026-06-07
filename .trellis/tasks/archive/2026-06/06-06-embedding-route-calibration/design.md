# Embedding Route Calibration Design

## Public Contract

- Add `smart-search route-calibrate --models CSV --format json|markdown|content`.
- Default models are the five known SiliconFlow candidates:
  `Qwen/Qwen3-Embedding-8B`, `Qwen/Qwen3-Embedding-4B`,
  `Qwen/Qwen3-Embedding-0.6B`, `Pro/BAAI/bge-m3`,
  `BAAI/bge-large-zh-v1.5`.
- Add config keys:
  `INTENT_EMBEDDING_THRESHOLD` default `0.74` and
  `INTENT_EMBEDDING_MARGIN` default `0.05`.

## Data Flow

- Calibration dataset lives in source as static, testable route examples.
- Service layer evaluates semantic-only by embedding all examples for a model,
  choosing top capability by max cosine score, then sweeping thresholds and
  margins to maximize Macro-F1.
- Full-route evaluation reuses `IntentRouter.route()` with the candidate model
  and recommended threshold/margin while preserving rules/classifier behavior.
- CLI formatting renders the same result in JSON, markdown, and compact content.

## Routing Changes

- `_semantic_route()` should return per-capability scores plus top capability,
  top score, second score, margin, threshold, and minimum margin.
- `route()` records semantic scores/signals for observability.
- Only add the top semantic capability when threshold and margin both pass.
- If threshold passes but margin fails, record an ambiguous semantic reason and
  do not add a capability.

## Compatibility

- Existing config defaults preserve the current threshold unless the user sets a
  new value.
- Optional embeddings/classifier remain fail-open. Calibration must record model
  failures per model and continue.
- Classifier provider choices remain ignored; router output remains capabilities
  only.
