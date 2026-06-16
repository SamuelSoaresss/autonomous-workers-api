# Documento de Regras de Domínio

Este documento descreve a modelagem de entidades e as restrições de negócio da Plataforma de Autônomos, definindo o comportamento esperado do sistema e garantindo a consistência dos dados.

---

## 3.1 Modelagem de Entidades

*   **Usuario:** Representa os participantes da plataforma. 
    *   **Atributos:** `id` (UUID, obrigatório), `nome` (String, obrigatório), `email` (String, obrigatório, unique), `is_worker` (Boolean, obrigatório).
    *   **Relacionamentos:** 1:N com `ServicoOferecido` (apenas se for worker) e 1:N com `Contratacao` (como cliente).
*   **ServicoOferecido:** Representa o serviço disponibilizado por um trabalhador.
    *   **Atributos:** `id` (UUID, obrigatório), `worker_id` (UUID, FK, obrigatório), `titulo` (String, obrigatório), `preco_base` (Numeric, obrigatório, >= 0).
    *   **Relacionamentos:** N:1 com `Usuario` (o worker que o criou) e 1:N com `Contratacao`.
*   **Contratacao:** Representa o agendamento de um serviço entre um cliente e um worker.
    *   **Atributos:** `id` (UUID, obrigatório), `cliente_id` (UUID, FK), `servico_id` (UUID, FK), `status` (Enum, obrigatório), `motivo_cancelamento` (String, opcional, exigido apenas no cancelamento).
    *   **Relacionamentos:** N:1 com `Usuario` (cliente) e N:1 com `ServicoOferecido`.
*   **AuditoriaContratacao:** Tabela de histórico para rastrear transições de estado.
    *   **Atributos:** `id`, `contratacao_id`, `status_anterior`, `status_novo`, `data_alteracao`.

### Máquina de Estados da Entidade `Contratacao`
A entidade de Contratação segue o seguinte ciclo de vida:
`SOLICITADA` ➡️ `EM_ANDAMENTO` ➡️ `CONCLUIDA`
Ou pode ser interrompida:
`SOLICITADA` / `EM_ANDAMENTO` ➡️ `CANCELADA`

*(Nota: `CONCLUIDA` e `CANCELADA` são estados terminais).*

---

## 3.2 Regras de Negócio

### Regra 1: Restrição de Criação de Serviço
*   **Identificador:** RN-001
*   **Nome:** Apenas autônomos podem criar serviços
*   **Gatilho:** Ao criar um novo serviço via API (POST /servicos/).
*   **Pré-condição:** O usuário que está tentando criar o serviço deve existir no banco e possuir a flag `is_worker == True`.
*   **Ação:** O sistema vincula o novo serviço ao perfil do trabalhador e o persiste no banco.
*   **Violação:** Retorna HTTP 400 com payload: `{"error": "INVALID_WORKER_PROFILE", "message": "Apenas usuários 'worker' podem criar serviços.", "details": null}`

### Regra 2: Consistência Financeira do Serviço
*   **Identificador:** RN-002
*   **Nome:** Preço do serviço não pode ser negativo
*   **Gatilho:** Ao tentar criar ou atualizar as informações de um serviço.
*   **Pré-condição:** O valor enviado no campo `preco_base` deve ser maior ou igual a zero (validação Pydantic).
*   **Ação:** A requisição é processada normalmente.
*   **Violação:** Retorna HTTP 422 com payload: `{"error": "VALIDATION_ERROR", "message": "Os dados enviados são inválidos.", "details": [{"campo": ["body", "preco_base"], "mensagem": "Value error, O preço base deve ser maior que zero."}]}`

### Regra 3: Integridade de Contas (E-mail Único)
*   **Identificador:** RN-003
*   **Nome:** E-mail de usuário não pode ser duplicado
*   **Gatilho:** Ao cadastrar um novo usuário na plataforma (POST /usuarios/).
*   **Pré-condição:** O campo `email` não deve existir previamente na base de dados (Unique Constraint).
*   **Ação:** O sistema cria a conta e retorna os dados do usuário.
*   **Violação:** Retorna HTTP 400 com payload: `{"error": "EMAIL_ALREADY_EXISTS", "message": "Já existe um usuário cadastrado com este e-mail.", "details": {"email_informado": "teste@teste.com"}}`

### Regra 4: Imutabilidade de Estados Terminais
*   **Identificador:** RN-004
*   **Nome:** Bloqueio de alteração em serviços finalizados
*   **Gatilho:** Ao tentar atualizar o status de uma contratação.
*   **Pré-condição:** O status atual da contratação não pode ser `CONCLUIDA` nem `CANCELADA`.
*   **Ação:** O sistema efetua a transição de estado solicitada (ex: de SOLICITADA para EM_ANDAMENTO).
*   **Violação:** Retorna HTTP 400 com payload: `{"error": "TERMINAL_STATE_REACHED", "message": "Não é possível alterar uma contratação que já foi concluída ou cancelada.", "details": {"status_atual": "CANCELADA"}}`

### Regra 5: Transparência em Cancelamentos
*   **Identificador:** RN-005
*   **Nome:** Cancelamento exige justificativa
*   **Gatilho:** Ao atualizar o status de uma contratação especificamente para `CANCELADA`.
*   **Pré-condição:** O payload da requisição deve obrigatoriamente conter o campo texto `motivo_cancelamento` preenchido.
*   **Ação:** O sistema cancela a contratação e grava o motivo na base, além de gerar o log de auditoria.
*   **Violação:** Retorna HTTP 400 com payload: `{"error": "MISSING_CANCEL_REASON", "message": "O motivo do cancelamento é obrigatório ao cancelar uma contratação.", "details": null}`