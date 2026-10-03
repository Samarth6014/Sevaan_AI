.PHONY: setup seed test backend frontend validate
setup:
	python3 -m venv .venv && .venv/bin/pip install -r backend/requirements.txt && cd frontend && npm install
seed:
	python3 -m scripts.seed
validate:
	python3 -m scripts.validate_rules
test:
	python3 -m pytest -q
backend:
	python3 -m uvicorn backend.app:app --reload --port 8000
frontend:
	cd frontend && npm run dev
