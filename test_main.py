from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add():
    response = client.post("/add", json={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_subtract():
    response = client.post("/subtract", json={"a": 5, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 2


def test_multiply():
    response = client.post("/multiply", json={"a": 4, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 12


def test_divide():
    response = client.post("/divide", json={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_divide_by_zero():
    response = client.post("/divide", json={"a": 10, "b": 0})
    assert response.status_code == 400


def test_power():
    response = client.post("/power", json={"a": 2, "b": 10})
    assert response.status_code == 200
    assert response.json()["result"] == 1024
