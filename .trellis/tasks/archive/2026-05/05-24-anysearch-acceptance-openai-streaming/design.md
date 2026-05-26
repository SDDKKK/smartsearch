# Design

## Architecture

OpenAI-compatible streaming remains part of `main_search`; it changes transport mode only for the configured Chat Completions relay. It must not affect xAI Responses or fabricate additional main-search providers.

AnySearch is introduced as an experimental provider surface. It is represented as optional `vertical_search` capability metadata and exposed through explicit CLI commands. It is not inserted into existing same-capability fallback chains until acceptance data proves a narrower integration is safe.

## Contracts

- `OPENAI_COMPATIBLE_STREAM` is a boolean config value. CLI `--stream` / `--no-stream` wins over config for the current `search` invocation.
- `AnySearchProvider` calls `POST {ANYSEARCH_API_URL}` with JSON-RPC 2.0:
  - `method = "tools/call"`
  - `params.name` is `list_domains`, `search`, `extract`, or `batch_search`
  - `params.arguments` carries command-specific arguments.
- AnySearch result shape returned by service/CLI:
  - `ok`, `provider`, `tool`, `content`, `raw_content`, `results`, and `elapsed_ms` on success.
  - `ok=false`, `error_type`, `error`, `provider`, `tool`, and `elapsed_ms` on failure.
  - `result.isError=true` maps to `error_type="provider_error"`.

## Boundary Rules

- `standard` minimum profile continues to require only `main_search`, `docs_search`, and `web_fetch`.
- `get_capability_status()` may show `vertical_search`, but its status does not affect minimum-profile pass/fail.
- Deep planner routing is not changed in this task.
- Live acceptance tests are opt-in and must not depend on local saved config.
