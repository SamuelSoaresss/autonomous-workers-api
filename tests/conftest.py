import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    # Cria um cliente virtual que simula o navegador/Swagger batendo na API
    with TestClient(app) as c:
        yield c