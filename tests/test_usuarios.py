import uuid

def test_criar_usuario_com_sucesso(client):
    payload = {
        "nome": "Professor Avaliador",
        "email": f"avaliador_{uuid.uuid4()}@teste.com",
        "is_worker": False
    }
    response = client.post("/usuarios/", json=payload)
    assert response.status_code == 201

def test_criar_trabalhador_com_sucesso(client):
    payload = {
        "nome": "João Encanador",
        "email": f"joao.encanador_{uuid.uuid4()}@teste.com",
        "is_worker": True
    }
    response = client.post("/usuarios/", json=payload)
    assert response.status_code == 201

def test_erro_ao_criar_usuario_sem_email(client):
    payload = {
        "nome": "Usuário Sem Email",
        "is_worker": False
    }
    response = client.post("/usuarios/", json=payload)
    assert response.status_code == 422
    assert response.json()["error"] == "VALIDATION_ERROR"

def test_erro_ao_criar_usuario_com_email_invalido(client):
    payload = {
        "nome": "Email Errado",
        "email": "isso-nao-e-um-email",
        "is_worker": False
    }
    response = client.post("/usuarios/", json=payload)
    assert response.status_code == 422

def test_listar_usuarios(client):
    response = client.get("/usuarios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)