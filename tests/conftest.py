import os, tempfile
os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mkdtemp()}/test.db"
os.environ["LLM_PROVIDER"] = "mock"
import pytest
from fastapi.testclient import TestClient
from backend.app import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def login(client, phone, role="citizen"):
    r = client.post("/api/auth/verify", json={"phone": phone, "otp": "123456", "role": role})
    assert r.status_code == 200
    return {"Authorization": f"Bearer {r.json()['token']}"}


@pytest.fixture()
def citizen(client):
    return login(client, "9000000001")
