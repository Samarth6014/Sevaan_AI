# ScholarPath: project structure

Each folder has one owner (A to E, see README Team section). `[later]` = created empty with a README. An enhancement is a new file or folder, not an edit to shared code.

```
scholarpath/
├── README.md  .env.example  .gitignore  Makefile
├── .github/workflows/ci.yml        # pytest, validate_rules, frontend build            (A)
|
├── docs/
|   ├── decisions.md                # FROZEN contracts                                  (E writes, A edits)
|   ├── architecture.md             # extension guide                                   (A)
|   ├── blueprint.pdf  demo_script.md                                                   (E)
|
├── packs/                          # SERVICE PACKS: content only, no code              (E)
|   ├── scholarships/
|       ├── pack.json               # id, name, languages, workflow, connector
|       ├── schemes/*.json          # rule files: source URL, verified, faqs, where_to_get
|       ├── source/schemes_raw.csv
|
├── fixtures/                       # demo and test material                            (E)
|   ├── sample_docs/{clean,noisy}/
|   ├── audio/<language>/
|   ├── cache/                      # pre-cached STT, TTS, extractions
|
├── backend/
|   ├── app.py                      # builds the app, registers routers                 (A)
|   ├── core/                       # config, db, logging, errors, pii masking          (A)
|   ├── models/                     # DB tables, one file per entity                    (A)
|   ├── schemas/                    # FROZEN API models                                 (A)
|   ├── auth/                       # mock OTP, session token, roles                    (A)
|   ├── api/                        # citizen routers                                   (A)
|   ├── admin/                      # cases, analytics, scheme edit                     (A)
|   ├── agent/                                                                          (A)
|   |   ├── loop.py  llm.py  guardrails.py  trace.py
|   |   ├── workflows/              # base.py, scholarship.py
|   |   ├── prompts/                # base.py, en.yaml, <lang>.yaml
|   |   ├── tools/                  # one file per tool + registry
|   ├── rules/                      # pure Python, NO LLM imports                       (B)
|   ├── speech/                     # adapter, cache, providers/                        (B)
|   ├── documents/                  # reader, prefill, validate                         (B)
|   ├── connectors/                 # base interfaces; mock/ now; real/ [later]         (A, E)
|   ├── channels/                   # web now; whatsapp, sms, ivr [later]               (A)
|
├── tests/                          # rules, documents, agent, security, connectors
├── eval/                           # gen_personas, run_eval, adversarial cases         (B)
├── reports/                        # eval report, accessibility scores                 (B, C)
|
├── frontend/
|   ├── public/sw.js  manifest      # PWA service worker and manifest
|   ├── e2e/                        # keyboard, axe and lite-mode tests                 (C)
|   ├── src/
|       ├── app/                    # shell: router, layout, guards                     (C)
|       ├── shared/                 # api client, ui kit, a11y, display, i18n           (C; E for strings)
|       ├── features/               # one self-contained folder per feature
|           ├── auth catalogue scheme chat voice review                                 (C)
|           ├── cases documents consent assisted notifications feedback trace admin     (D)
|
├── scripts/                        # seed, validate_rules, gen_sample_docs, precache_demo
```

## Dependency rules
1. Frontend talks only to `/api/*` via `shared/api/client.ts`.
2. One frontend feature never imports another; shared code goes in `shared/`.
3. The agent reaches everything through `agent/tools/`; guardrails live only in `guardrails.py`.
4. `rules/` imports nothing from agent, speech or LLM code.
5. The agent uses `connectors/base.py`, never a specific mock or real portal.
6. `packs/` is data only.
7. `submit_application` is the only code that submits, and it checks the confirmation token first.
8. Nobody edits another owner's folder without asking.

## Frozen files (only A edits, after telling the team)
`docs/decisions.md`, `backend/schemas/`, `backend/rules/schema.py`, tool contracts in `backend/agent/tools/base.py`.
