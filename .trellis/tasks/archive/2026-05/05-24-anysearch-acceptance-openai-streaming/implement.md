# Implementation Plan

## 1. Streaming

- Add config property/key for `OPENAI_COMPATIBLE_STREAM`.
- Thread an optional stream override from CLI `search` into `service.search()` and OpenAI-compatible provider construction/calls.
- Switch only OpenAI-compatible `search()` and `fetch()` between `_execute_completion_with_retry()` and `_execute_stream_with_retry()`.
- Update setup, config display, doctor output, docs, and tests.

## 2. AnySearch Experimental Surface

- Add `providers/anysearch.py` with JSON-RPC request helper, text extraction, result parsing, and error normalization.
- Add service helpers for `anysearch_domains`, `anysearch_search`, `anysearch_extract`, and `anysearch_batch`.
- Add CLI commands and aliases without changing existing fallback chains.
- Add `vertical_search` optional capability status.
- Add docs and skill contract updates in both public and packaged skill trees.

## 3. Verification

- Run focused pytest for provider, service, CLI, and smoke tests.
- Run source checkout mock smoke.
- Run compile/diff checks if time permits.
- If live AnySearch validation is run, scan for the exact key substring before commit.
