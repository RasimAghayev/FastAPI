# Improvement Roadmap — FastAPI

Phase 3 plan (docs). Execution requires appropriate approvals/gates and must follow per-phase verification standards in `PROMPT.md`/`CLAUDE.md`.

## Guiding goals
1. Make builds/tests reproducible and containerized (`make verify` as contract).
2. Upgrade runtime and dependencies to latest stable with baseline-backed safety.
3. Improve structure, security posture, and operability proportionate to a small CRUD service.
4. Add CI and tests to prevent regressions.
5. Keep existing business behavior unless a breaking change is explicitly approved (Gate 5).

## Phase-by-phase roadmap (4–11)

### Phase 4 — Git hygiene (`git-steward`)
- **Scope:** full-history `gitleaks` scan; add `.gitignore`, `.gitattributes`, secret-scan pre-commit hook; review/delete branches per policy; document PR/bot-PR handling.
- **Gate/notes:** `master→main` conversion requires **Gate 4** (needs approval). History rewrite/force-push requires **Gate 1** if ever needed. Archived/fork policy N/A (repo not archived/forked).
- **Artifacts:** handoff with deleted-branch SHAs (if any), scan results (redacted).

### Phase 5 — Container baseline (`container-engineer`)
- **Scope:** multi-stage `Dockerfile` (base/deps/build/test/runtime), `.dockerignore`, `docker-compose.yml`, `Makefile` (`build`, `test`, `verify`, `up` depends on `verify`, `run`, `down`, etc. as applicable), `.env.example`.
- **Baseline:** run existing tests in `test` stage (none today) and add minimal **characterization tests** for current CRUD/health behavior; capture `docs/BASELINE.md` (results, coverage snapshot, key API behavior).
- **Exit:** `make verify` green or pre-existing failures documented; `make up` gated on verify.

### Phase 6 — Upgrade to latest (`upgrader`)
- **Scope:** introduce/maintain manifest+lock; upgrade in order (runtime/base image → framework/libs → dev tools/actions) using registry-confirmed latest stable versions; migrate breaking changes (notably Pydantic v1→v2, FastAPI/Starlette/Tortoise majors as applicable).
- **Controls:** one logical step per commit, `make verify` after each; revert only failing step if blocked and record blocker. Update/close dependency-bot PRs if present (none currently).
- **Gate:** **Gate 5** for breaking public API/contract changes. Dependabot config added/verified per PROMPT if missing.

### Phase 7 — Dead code & restructure (`cleaner`)
- **Scope:** remove committed runtime artifacts from tracking where appropriate (`store.db*`, `__pycache__`), align layout with modern conventions, remove unused/dead code and compat shims, fix minor issues (naming/docs nits) with verification after each batch.
- **Risk control:** preserve behavior against Phase 5 baseline.

### Phase 8 — Architecture (`architect`)
- **Scope:** apply KISS/YAGNI; introduce light structure (e.g. app factory/config, routers, schemas, db/session module) only with justification and ADRs if warranted.
- **Likely n/a / limited:** DDD bounded contexts/aggregates and EDA/outbox are **not** justified for this single-entity CRUD demo—document "not applied" reasons. SOLID only where complexity emerges.
- **Exit:** architecture decisions recorded (update `docs/ARCHITECTURE.md`/ADRs as needed); `make verify` green.

### Phase 9 — Hardening (`hardener`)
- **Scope:** env-driven config (12-factor basics), input validation, error handling, CORS/rate-limit considerations as appropriate, `/health/live` and `/health/ready`, structured logging basics, dependency/secret hygiene, dual-mode friendliness where cheap (`MODE`/stubs if relevant).
- **Security:** address P0–P3 items proportionately; document findings and fixes. No real secrets/environments required.
- **Exit:** security/ops checklist with results; `make verify` green.

### Phase 10 — CI/CD (`ci-engineer`)
- **Scope:** GitHub Actions pipeline per runner-time standard (parallel cheap checks, Docker-based tests/build, cache, pinned actions, least privilege, timeouts, concurrency control).
- **Target:** PR pipeline ≤ 10 min (measure real run, record in `docs/TEST_REPORT.md` or handoff/evidence).
- **Exit:** real green CI run linked in handoff, or overrun documented with causes.

### Phase 11 — Tests (`tester`)
- **Scope:** unit/integration/API tests for CRUD, validation, and error paths (404, bad input) run in Docker; regression against `docs/BASELINE.md`; `docs/TESTING_STRATEGY.md` and `docs/TEST_REPORT.md` with honest coverage and TC IDs.
- **Rule:** production bugs found during testing are reported to Orchestrator (not fixed in-phase) per R8.

## Later phases (ecosystem context)
- **P12 (merge):** FastAPI not flagged as small-merge candidate in index; likely `n/a` unless reclassified.
- **P13 (shared lib):** extract only if same logic appears in ≥3 repos (unlikely for this standalone demo).
- **P14 (rename):** Gate 2 if pursued.
- **P15 (docs/manifest/diagrams):** standardize docs, add `repo-manifest.yaml`, ensure diagrams match reality.
- **P16/17:** platform/report as applicable ecosystem-wide.

## Priority order (risk/enablement)
1. **P4/P5:** hygiene + reproducible container baseline and characterization (enables safe change).
2. **P6:** dependency/runtime upgrades to latest stable (largest risk reduction).
3. **P7/P8:** cleanup and right-sized structure.
4. **P9–P11:** hardening, CI, comprehensive tests.
5. **P15+:** documentation/manifest alignment.

## Approval and gating summary
- **Gate 10 (this plan):** **needs approval** for FastAPI (no pre-approval recorded in `projects/info/state/APPROVALS.md`).
- **Gate 4:** master→main — needs approval if executed.
- **Gate 5:** breaking public contract/API during upgrade/refactor — needs approval if triggered.
- **Gates 1/2/6/9:** not expected from current scope; park and request approval if triggered.