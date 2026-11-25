# automaton

A three-tier notes service — nginx → backend → database — rebuilt the way a platform team would: hardened containers, health-gated startup, self-healing restarts, CI on every push, and a scripted chaos drill. The goal is a machine that keeps running by itself. *(Subject 01, DevOps portfolio track — the failure-half companion to Inception's features-half.)*

## Architecture *(phases 3.4, 4.2; nginx/db arrive in steps 7 & 5)*

```text
browser ──► nginx ──► backend (gunicorn) ──► MariaDB
(future)   (future)   (built)               (future: volume + schema)
```

* **backend** — Python 3.13 + Flask. Application factory (`create_app`) so tests and production share one build path. Hosted by gunicorn, 2 prefork workers, logs on stdout/stderr. *(phase 3.4, 4.2)*
* **storage seam** — the app talks to `NoteStore` (`add`/`all`/`get`/`delete`), in-memory today; the MariaDB swap in step 5 changes no route. *(phase 3.3)*
* **database** — MariaDB on a named volume, init schema on first boot only. *(step 5, planned)*
* **nginx** — the only published port; proxies to backend with standard proxy headers. *(step 7, planned)*

## Stack, and why *(phase: market research before 3.1)*

**Python + Flask + gunicorn + MariaDB + nginx.** Python because it is the most recruiter-demanded language worldwide (~46% of recruiters) and appears in Morocco DevOps job ads alongside Bash. The subject is about operations — the language is chosen by the market, not by novelty.

## Status

- [x] Notes API: 5 routes, edge validation, 7 pytest tests green *(phase 3.5–3.6)*
- [x] Gunicorn handover: 100/100 requests answered 200 under 10-way parallel load *(phase 4.2)*
- [x] Guilty baseline measured before any hardening *(phase 4.1)*
- [ ] Multi-stage, non-root, slim image *(steps 4.3–4.5, in progress)*
- [ ] MariaDB + volume, health gates, nginx, caps, Makefile, chaos, CI *(steps 5–11)*

## Quick start *(current phase)*

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements-dev.txt
pytest backend                      # 7 tests, the contract guard
cd backend && docker build -t notes-backend:naive .
docker run --rm -d -p 8000:8000 --name notes notes-backend:naive
curl -i localhost:8000/healthz
```

*(The one-command `make up` story arrives in step 9.)*

## Decisions

* **Pin everything:** dependencies `==`-pinned, base image `python:3.13-bookworm` — reproducibility over convenience. *(phase 3.2, 4.1)*
* **Storage behind a swappable `NoteStore` interface** — the seam that makes the database swap a non-event. *(phase 3.3)*
* **`/healthz` exists from day one:** future container healthcheck, smoke-test and chaos probe target. *(phase 3.4)*
* **Validate at the edge, never trust the client** — corrupt input is an assumed failure, refused politely with `400`. *(phase 3.5)*
* **Guilty baseline first, measured:** 1.04 GB, runs as root, dev server warning caught in-container. Improvements get numbers, not vibes. *(phase 4.1)*
* **Gunicorn 23.0.0, 2 prefork workers, logs on stdout/stderr** (12-factor, R5 seeded). Worker-kill drill: master respawned the dead worker — self-healing at process level; the same philosophy scales to containers in R4/R7. *(phase 4.2)*
* **Rootless Docker on school PCs:** daemon per-PC, data in `/goinfre`. CPU limits not enforceable in rootless mode — documented, memory-only caps. *(phase 2)*
* **non-root user:** notes (UID 1000), least privilege; .dockerignore gates the context — caches, tests, dev deps, and .env can never enter an image. *(phase 4.4)*

## Evidence

| Claim | Number | Phase |
| :--- | :--- | :--- |
| Naive image size (before hardening) | 1.04 GB | 4.1 |
| Parallel load test | 100 × 200, 0 failures | 4.2 |
| Test suite | 7 passed in ~0.1 s | 3.6 |
| Red-proof (suite has teeth) | 1 surgical failure on sabotage | 3.7 |
| Multi-stage image | 137 MB (−87% vs 1.04 GB) | 4.3