# API Plataforma de Autônomos

API RESTful desenvolvida com **FastAPI** e **PostgreSQL** para a gestão de trabalhadores autônomos e contratação de serviços. Este é um projeto acadêmico focado na aplicação de boas práticas de Engenharia de Software, modelagem de dados e testes automatizados.

---

##  Tecnologias e Ferramentas

* **Linguagem:** Python 3.11
* **Framework Web:** FastAPI
* **Banco de Dados:** PostgreSQL
* **ORM e Migrations:** SQLAlchemy + Alembic
* **Validação de Dados:** Pydantic v2
* **Testes Automatizados:** Pytest + httpx
* **Infraestrutura:** Docker e Docker Compose

---

##  Principais Funcionalidades e Requisitos Atendidos

* **CRUD Completo:** Rotas para criação e listagem de Usuários e Serviços.
* **Regras de Negócio Blindadas:** 
  * Apenas usuários com o perfil `is_worker=True` podem oferecer serviços.
  * O sistema bloqueia a criação de serviços com preços base negativos.
* **Tratamento Global de Exceções (Global Handler):** Erros de validação (HTTP 422) e exceções internas são interceptados e formatados em um payload padronizado, seguro e amigável para o front-end.
* **Evolução de Banco de Dados:** Histórico de alterações versionado pelo Alembic, contendo:
  1. Estrutura inicial do banco de dados.
  2. Adição da coluna `motivo_cancelamento` justificada por necessidades de negócio.
  3. Criação da tabela `auditoria_contratacoes` para rastreabilidade de mudanças de status.
* **Suíte de Testes:** Mais de 10 testes de integração cobrindo caminhos de sucesso (HTTP 200/201), falhas de validação e restrições de integridade de dados (e-mails únicos).

---

##  Como Executar o Projeto Localmente

O ambiente da aplicação é totalmente containerizado. Certifique-se de ter o **Docker** e o **Docker Compose** instalados na sua máquina.

### 1. Subir os Contêineres
Na raiz do projeto, execute o comando abaixo para construir as imagens e iniciar o banco de dados e a API:

```bash 
docker compose up --build
``` 

2. Acessar a Documentação Interativa (Swagger)
Com o servidor rodando, abra o seu navegador e acesse:
 ```bash
http://localhost:8000/docs
 ```

   Executando as Migrations (Alembic)
Para que o banco de dados receba todas as tabelas e colunas corretamente, é necessário aplicar as migrações após subir o contêiner pela primeira vez.

Abra um novo terminal e execute: 
```bash
docker compose exec api alembic upgrade head
```

   Rodando os Testes Automatizados
Para validar o funcionamento da aplicação e garantir que nenhuma regra de negócio foi quebrada, rode a suíte completa de testes isolada dentro do contêiner: 
```bash
 docker compose exec api pytest 
```


 ## 📊 Diagrama ER (Entidade-Relacionamento)

+-------------------+       +-----------------------+
|      Usuario      |       |    ServicoOferecido   |
+-------------------+       +-----------------------+
| id (UUID)         |<-----\| id (UUID)             |
| nome (String)     |      || worker_id (FK)        |
| email (String)    |      || titulo (String)       |
| is_worker (Bool)  |      || preco_base (Numeric)  |
+-------------------+      /+-----------------------+
        |                 /            |
        |                /             |
        v               /              v
+-------------------+  /    +------------------------+
|    Contratacao    | /     | AuditoriaContratacao   |
+-------------------+/      +------------------------+
| id (UUID)         |       | id (UUID)              |
| cliente_id (FK)   |       | contratacao_id (FK)    |
| servico_id (FK)   |------>| status_anterior (Str)  |
| status (Enum)     |       | status_novo (Str)      |
| motivo_cancel (Str|       | data_alteracao (Date)  |
+-------------------+       +------------------------+

## Cenários de Borda e Decisões de Design

* **O que acontece ao deletar um worker com serviços ativos?** 
  *Decisão:* Foi Implementado a restrição padrão ou `ondelete="CASCADE"`. Se um trabalhador for removido, seus serviços também são. Porém, se houverem *Contratações* ligadas a esse serviço, o banco de dados bloqueia a exclusão para manter o histórico financeiro e de auditoria intacto.
* **O que acontece se modificarem uma entidade em estado terminal?** 
  *Decisão:* Se uma contratação estiver `CONCLUIDA` ou `CANCELADA`, a API bloqueia qualquer nova transição de status retornando HTTP 400. Estados terminais são imutáveis para garantir a confiabilidade dos registros.
* **Race Condition (Modificação Simultânea):**
  *Decisão:* Caso dois clientes tentem contratar um serviço limitante exatamente ao mesmo tempo, a aplicação delega a resolução para o isolamento transacional do PostgreSQL (ACID), que travará a linha em disputa e garantirá que apenas a primeira transação seja commitada com sucesso.
