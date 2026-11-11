# 0001 — Usage data is never public

- **Decision:** the usage review (prompts, counts, coaching) renders only to gitignored `local/usage.html`; the public `docs/index.html` is built from `data/runs/` and the report index and never reads `data/usage/`.
- **Context:** usage metrics and `usage-prompts.csv` hold Greg's own prompt text, which can include personal and client-adjacent content; the trends page is public and linked from the RANGE network.
- **Options:** (a) one page with a usage tab, rejected as one bad merge from a leak; (b) a separate private repo, more machinery than needed; (c) separate render paths with a test, chosen.
- **Enforced by:** `.gitignore` (`data/usage/`, `local/`), no remote, and a pytest that renders both pages and asserts no fixture prompt string appears in `docs/index.html`. Superseded only by a new ADR.
