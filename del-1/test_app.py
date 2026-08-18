from app import app


def test_index():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert data["application"] == "JensenStore API"
    assert data["status"] == "running"
    assert data["version"] == "1.0.0"


def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "healthy"}
