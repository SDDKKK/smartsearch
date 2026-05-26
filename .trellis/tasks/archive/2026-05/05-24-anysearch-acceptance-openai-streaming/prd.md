# SmartSearch AnySearch acceptance and OpenAI-compatible streaming

## Goal

Implement OpenAI-compatible streaming as an opt-in relay compatibility feature, and add an experimental AnySearch provider/CLI surface for acceptance testing and capability-boundary evaluation. AnySearch must not enter the default `web_search` fallback chain or `standard` minimum profile in this task.

## Requirements

- **R1**: OpenAI-compatible streaming is opt-in and backward compatible.
  - [x] `OPENAI_COMPATIBLE_STREAM` defaults to false and accepts the existing boolean style (`true/1/yes`).
  - [x] `smart-search search` supports `--stream` and `--no-stream`; CLI flags override config.
  - [x] Only OpenAI-compatible `search()` and `fetch()` use the stream toggle; URL description and source ranking remain non-streaming.

- **R2**: AnySearch is added as an experimental acceptance surface, not a default route.
  - [x] Add config for `ANYSEARCH_API_URL`, `ANYSEARCH_API_KEY`, and `ANYSEARCH_TIMEOUT_SECONDS`.
  - [x] Add explicit CLI commands for domains, search, extract, and batch calls.
  - [x] Normalize JSON-RPC `result.isError=true`, HTTP errors, timeouts, and batch size violations into stable CLI error results.
  - [x] Preserve raw markdown/text output and extract URL/title/snippet candidates when available.

- **R3**: Provider capability boundaries remain intact.
  - [x] No change to `main_search`, `docs_search`, `web_search`, or `web_fetch` fallback order.
  - [x] AnySearch is reported as an optional/experimental `vertical_search` capability when configured.
  - [x] AnySearch is not required by `SMART_SEARCH_MINIMUM_PROFILE=standard`.

- **R4**: Documentation and packaged skill contracts stay synchronized.
  - [x] Public README files document streaming and AnySearch as experimental vertical search.
  - [x] Repo-local and packaged `smart-search-cli` skill assets are updated consistently.

## Acceptance Criteria

- [x] Streaming unit tests cover default false, config true, CLI override, stream parser behavior, and non-stream regression.
- [x] AnySearch unit tests cover JSON-RPC success, `isError=true`, HTTP error, timeout, anonymous/key headers, URL extraction, raw structured results, and batch limit.
- [x] CLI tests cover new commands and config/setup surfaces.
- [x] `pytest tests/test_openai_compatible_provider.py tests/test_service.py tests/test_cli.py tests/test_smoke.py -q` passes.
- [x] `smart-search smoke --mock --format json` passes from the source checkout.
- [x] If the live AnySearch key is used, an exact-key secret scan returns no hits before commit.

## Notes

- Use the user-provided AnySearch key only for optional live validation. Do not save it in config, docs, fixtures, or task artifacts.
