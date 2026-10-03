# ScholarPath

Accessible digital public-service platform with a scholarship application agent
(24-hour hackathon, Agentic AI, "Accessible Digital Public Service Experience").
Built from Project Blueprint v2 (3 Oct 2026). **All government systems are simulated; all data is synthetic.**

## Quick start
```bash
make setup      # python venv + npm install
make seed       # create DB, validate rule files
make test       # pytest
make backend    # http://localhost:8000  (docs at /docs)
make frontend   # http://localhost:5173
```
Runs with no API keys: `LLM_PROVIDER=mock` and `USE_CACHED_DEMO=true` use a built-in rule-based
extractor and typed input. Add keys in `.env` for real LLM and speech.

## Team (owners, see PROJECT_STRUCTURE.md)
A tech lead (agent, api, auth, core) · B AI core (rules, speech, documents, eval) ·
C citizen frontend + a11y · D frontend part 2 (cases, consent, assisted, admin) · E data, packs, mocks, docs.

## Hard rules
1. Eligibility is decided by `backend/rules` (pure Python), never by the LLM.
2. `submit_application` is the only code that submits and it verifies the confirmation token first.
3. Everything government-side is a mock. The UI shows a "demo only" banner.
4. Not claimed: native app, real login, encryption at rest, SMS/IVR, real appointments.

## Status of rule files
Only `nmmss` has drafted rules (from the blueprint example) and every rule is `needs_verification`.
The other 9 are stubs: the engine returns **unknown** for them until a human fills the rules from the
official page and sets `verified=true`. Do not trust any value until verified.
