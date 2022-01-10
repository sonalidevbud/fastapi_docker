from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app

client = TestClient(app)


def test_ping():
    # assert True
    response = client.get("/")
    assert response.status_code == 200
    # assert response.json() == {"Hello": "World"}