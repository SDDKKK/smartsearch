# Local PATH wrapper and 1Password-backed provider environment

Use this reference when a host has a local `smart-search` wrapper that should run the user's fork checkout directly instead of a packaged/global install.

## Preferred agent entrypoint

For routine agent work, call `smart-search ...` from `PATH` after confirming it resolves to the host-local wrapper. Do not bypass the wrapper unless you are deliberately testing packaging or editing the checkout binary.

Verify the active wrapper before relying on live providers:

```bash
command -v smart-search
readlink -f "$(command -v smart-search)"
smart-search --version
smart-search doctor --format json
```

On Hiskens Netcup/default, the expected wrapper is:

```text
/home/Hiskens/.local/bin/smart-search
```

It runs the local fork checkout:

```text
/home/Hiskens/projects/smartsearch/.venv/bin/smart-search
```

with repository-managed 1Password references from:

```text
/home/Hiskens/projects/smartsearch/.env.tpl
```

The wrapper shape is:

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO="/home/Hiskens/projects/smartsearch"
CLI="$REPO/.venv/bin/smart-search"
ENV_FILE="$REPO/.env.tpl"
if [[ ! -x "$CLI" ]]; then
  echo "smart-search CLI not found or not executable: $CLI" >&2
  exit 127
fi
if [[ -f "$ENV_FILE" ]] && command -v op >/dev/null 2>&1; then
  exec op run --env-file "$ENV_FILE" -- "$CLI" "$@"
fi
exec "$CLI" "$@"
```

## Why this exists

- It keeps `smart-search ...` simple for agents and humans.
- It ensures commands use the local `SDDKKK/smartsearch` fork checkout, not an older packaged install.
- It keeps provider secrets in 1Password through `.env.tpl` instead of plaintext shell profiles or local config.
- It makes `doctor`, `search`, `fetch`, `route`, `deep`, and `research` behave consistently across sessions.

## Host variants

Other hosts may use the same contract with different paths:

- WSL may load `~/.config/hermes/smart-search.env` and then execute a checkout-local `.smart-search-python/bin/smart-search`.
- US-West/root may use `/root/.local/bin/smart-search` or `/usr/local/bin/smart-search -> /root/.local/bin/smart-search`, plus `~/.config/hermes/smart-search.env.tpl` with `op://` references.
- Netcup/default uses `/home/Hiskens/.local/bin/smart-search` plus `/home/Hiskens/projects/smartsearch/.env.tpl`.

In all cases, the contract is the same: `smart-search` from PATH should run the local fork checkout and inject the host's configured provider environment.

## When to bypass the wrapper

Use the checkout binary directly only for maintenance that must isolate the exact repo environment:

```bash
cd /home/Hiskens/projects/smartsearch
op run --env-file .env.tpl -- ./.venv/bin/smart-search doctor --format json
```

Use this for `.env.tpl` edits, provider-pool changes, package/release verification, or when diagnosing whether a PATH wrapper is masking a problem.

## Verification checklist

After creating or changing a wrapper, run:

```bash
command -v smart-search
smart-search --version
smart-search doctor --format json
smart-search route "smartsearch upstream fork merge strategy" --format json
smart-search fetch https://example.com --format content
smart-search search "SDDKKK smartsearch GitHub" --format content --timeout 90
```

Expected health on a configured host:

- `smart-search --version` matches the local checkout version.
- `doctor.ok` is `true` and `minimum_profile_ok` is `true`.
- OpenAI-compatible provider pools such as `grok-main,grok-backup` appear when configured.
- `route` returns JSON without live provider calls.
- `fetch` can retrieve Example Domains content.
- A short live `search` returns real results.

## Pitfalls

- Do not let PATH resolve to a packaged `smart-search` when the task depends on Hiskens' customized fork.
- Do not delete `.env.tpl`; local wrappers may depend on it for 1Password-backed provider secrets.
- Do not replace `op://` references with plaintext keys.
- Interactive `op signin` state may not be visible to a Hermes gateway process; use a service account token in the service environment when necessary.
- If `doctor` works in SSH but fails from Hermes, compare `command -v smart-search`, wrapper path, `OP_SERVICE_ACCOUNT_TOKEN`, and the gateway process environment.
