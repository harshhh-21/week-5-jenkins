from app import app, add


def test_add():
    assert add(2, 3) == 5


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"DevOps CI/CD Demo" in response.data


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
