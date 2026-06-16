import uuid

def test_criar_servico_com_sucesso(client):
    # 1. Cria um trabalhador dinâmico primeiro para termos um ID real e válido
    email_unico = f"marceneiro_{uuid.uuid4()}@teste.com"
    worker_payload = {
        "nome": "Marceneiro Teste",
        "email": email_unico,
        "is_worker": True
    }
    worker_res = client.post("/usuarios/", json=worker_payload)
    worker_id = worker_res.json()["id"]

    # 2. Usa o ID gerado para criar o serviço
    servico_payload = {
        "titulo": "Montagem de Móveis",
        "descricao": "Montagem de guarda-roupas e armários",
        "preco_base": 150.00,
        "ativo": True
    }
    res = client.post(f"/servicos/{worker_id}", json=servico_payload)
    
    assert res.status_code == 201
    assert res.json()["titulo"] == "Montagem de Móveis"

def test_erro_preco_negativo(client):
    # Passamos um ID falso qualquer apenas para bater na validação do Pydantic
    fake_id = str(uuid.uuid4())
    servico_payload = {
        "titulo": "Serviço Inválido",
        "preco_base": -50.00, # Preço negativo que programamos para dar erro
        "ativo": True
    }
    res = client.post(f"/servicos/{fake_id}", json=servico_payload)
    
    # O nosso Global Handler precisa devolver o 422 formatado
    assert res.status_code == 422
    assert res.json()["error"] == "VALIDATION_ERROR"

def test_erro_worker_nao_encontrado(client):
    fake_id = str(uuid.uuid4())
    servico_payload = {
        "titulo": "Serviço Fantasma",
        "preco_base": 100.00,
        "ativo": True
    }
    res = client.post(f"/servicos/{fake_id}", json=servico_payload)
    
    # O banco de dados não vai achar esse ID e deve retornar 404
    assert res.status_code == 404

def test_erro_usuario_nao_e_worker(client):
    # 1. Cria um cliente comum (is_worker = False)
    email_unico = f"cliente_{uuid.uuid4()}@teste.com"
    cliente_payload = {
        "nome": "Cliente Teste",
        "email": email_unico,
        "is_worker": False
    }
    cliente_res = client.post("/usuarios/", json=cliente_payload)
    cliente_id = cliente_res.json()["id"]

    # 2. Tenta burlar o sistema criando um serviço para ele
    servico_payload = {
        "titulo": "Serviço Ilegal",
        "preco_base": 100.00,
        "ativo": True
    }
    res = client.post(f"/servicos/{cliente_id}", json=servico_payload)
    
    # A regra de negócios precisa barrar com erro 400
    assert res.status_code == 400

def test_listar_servicos(client):
    res = client.get("/servicos/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)