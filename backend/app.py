from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.db import init_db
from backend.api import auth, schemes, cases, misc, mock
from backend.admin import routes as admin_routes


def build_app() -> FastAPI:
    app = FastAPI(title="ScholarPath (demo, simulated government systems)")
    app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])
    for r in (auth.router, schemes.router, cases.router, misc.router, mock.router, admin_routes.router):
        app.include_router(r)
    init_db()
    return app


app = build_app()
