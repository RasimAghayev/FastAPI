# Technical Debt — FastAPI

Phase 3 inventory. Items are derived from audit evidence; priorities align with P0–P3 findings in `projects/info/analysis/FastAPI.md`.

## Debt register
| ID | Priority | Category | Debt | Impact | Suggested phase | Notes |
|----|----------|----------|------|--------|-----------------|-------|
| TD-01 | P0 | Dependency management | No `pyproject.toml`/`requirements*.txt`/lockfile; ad-hoc installs | Non-reproducible builds, hidden drift, unsafe upgrades | P5, P6 | Must establish manifest+lock before/with upgrades |
| TD-02 | P0 | Framework/runtime currency | FastAPI 0.75 / Starlette 0.17 / Pydantic v1 / Tortoise 0.19 / Python 3.8-era | Security/compat risk, blocks modern ecosystem | P6 | Multi-step migration (esp. Pydantic v1→v2) |
| TD-03 | P1 | Repo hygiene | `store.db`, `store.db-shm`, `store.db-wal` committed; no `.gitignore` | Data leakage/conflicts, dirty history/worktree noise | P4, P7 | Decide tracking policy; prefer generated/local DB ignored |
| TD-04 | P1 | Verification | No automated tests, no characterization baseline in CI | Regressions likely during upgrade/refactor | P5, P11 | Add baseline first (P5) then full suite (P11) |
| TD-05 | P1 | Delivery/ops baseline | No Dockerfile, compose, Makefile, or CI workflows | No standard build/test/run contract | P5, P10 | Align to Docker/CI standards in PROMPT.md |
| TD-06 | P1 | Security controls | No auth, rate limiting, CORS policy, or env-based config | Unsafe if exposed beyond trusted local use | P9 | Scope proportional to intended use; document threat model |
| TD-07 | P1 | API/data modeling | `due_date` as string; limited validation; no list/pagination endpoint | Data quality and API ergonomics issues | P6–P9 | May affect contract (Gate 5 if breaking) |
| TD-08 | P2 | Code quality | Flat 2-file structure, minor naming typo (`TooIn`), doc drift risk | Maintainability/readability limits | P7, P8, P15 | Keep changes behavior-preserving per baseline |
| TD-09 | P2 | Git governance | Default branch `master`, no in-repo branch protection config/evidence | Process/governance gap | P4 | `master→main` requires Gate 4 approval |
| TD-10 | P2 | Database lifecycle | `generate_schemas=True` side effect; no migrations/backup strategy | Schema evolution and ops risk as app grows | P6–P9 | Introduce migrations if/when model evolves |
| TD-11 | P3 | Observability | No structured logs/metrics/tracing; single basic root endpoint only | Harder debugging and operations | P9 | Add `/health/live` & `/health/ready` in hardening |
| TD-12 | P3 | Licensing/compliance clarity | No root `LICENSE`; dependency licenses unconfirmed | Legal ambiguity for reuse/distribution | P15, P2 follow-up | Confirm and document |

## Known unknowns / unconfirmed
- Latest stable versions and vulnerability status not registry-verified in Phase 3.
- Full git history secret scan not run (planned Phase 4).
- Runtime behavior of OpenAPI doc paths and current endpoint edge cases not executed against a running server in this audit.

## Remediation principles
- Establish **baseline and verification** before risky upgrades (P5 → P6).
- Prefer **small, reversible commits** with `make verify` evidence in later phases.
- Do not claim resolution without verification (per CLAUDE.md/PROMPT.md).