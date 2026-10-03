# Extension guide
| I want to add | I add | I never touch |
|---|---|---|
| A new scheme | packs/scholarships/schemes/x.json, run `make validate` | API, UI, agent |
| A new language | frontend/src/shared/i18n/locales/<lang>.json, backend/agent/prompts/<lang>.yaml, one line in pack.json | agent loop, rules |
| A new service pack | packs/<id>/, agent/workflows/<id>.py, connectors/mock/<portal>.py | core agent, auth, admin |
| A new agent tool | agent/tools/<tool>.py, register in tools/__init__.py, update decisions.md, add a test | other tools |
| A new channel | channels/<x>.py plus a webhook route | agent, rules |
| Real NSP/DigiLocker | connectors/real/<x>.py, CONNECTOR_MODE=real | agent, UI |
