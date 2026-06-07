# Implementation Plan

1. Load backend and shared Trellis specs.
2. Add config keys/properties and doctor/router status fields.
3. Update `IntentRouter` semantic threshold/margin logic and tests.
4. Add calibration dataset and service evaluation helpers.
5. Add `route-calibrate` CLI parser, dispatcher, and formatters.
6. Update README, README.zh-CN, public skill, packaged skill, and CLI contract.
7. Run focused tests, then full validation:
   - `.venv\Scripts\python.exe -m pytest tests -q`
   - `.venv\Scripts\python.exe -m smart_search.cli regression`
   - `.venv\Scripts\python.exe -m smart_search.cli smoke --mock --format json`
   - `.venv\Scripts\python.exe -m compileall -q src tests`
   - `git diff --check`
