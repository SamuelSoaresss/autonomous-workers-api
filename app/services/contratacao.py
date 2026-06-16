from sqlalchemy.orm import Session
from fastapi import HTTPException
import uuid

from app.models.contratacao import Contratacao, StatusContratacao
from app.models.servico import ServicoOferecido
from app.models.auditoria import AuditoriaContratacao
from app.schemas.contratacao import ContratacaoCreate, ContratacaoStatusUpdate

def criar_contratacao(db: Session, contratacao_in: ContratacaoCreate):
    servico = db.query(ServicoOferecido).filter(ServicoOferecido.id == contratacao_in.servico_id).first()
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
        
    # RN-003: Prevenção de auto-contratação
    if servico.worker_id == contratacao_in.cliente_id:
        raise HTTPException(
            status_code=400,
            detail={"error": "SELF_CONTRACT_NOT_ALLOWED", "message": "Um trabalhador não pode contratar o próprio serviço."}
        )
        
    # Inicia a contratação no estado da máquina: SOLICITADA
    db_contratacao = Contratacao(**contratacao_in.model_dump(), status=StatusContratacao.SOLICITADA)
    db.add(db_contratacao)
    db.commit()
    db.refresh(db_contratacao)
    return db_contratacao

def atualizar_status_contratacao(db: Session, contratacao_id: str, dados_update: ContratacaoStatusUpdate):
    contratacao = db.query(Contratacao).filter(Contratacao.id == contratacao_id).first()
    
    if not contratacao:
        raise HTTPException(status_code=404, detail="Contratação não encontrada.")

    status_atual = contratacao.status

    # Regra de Negócio (RN-004): Imutabilidade de Estados Terminais
    if status_atual in [StatusContratacao.CONCLUIDA, StatusContratacao.CANCELADA]:
        raise HTTPException(
            status_code=400, 
            detail={
                "error": "TERMINAL_STATE_REACHED",
                "message": "Não é possível alterar uma contratação que já foi concluída ou cancelada.",
                "details": {"status_atual": status_atual.value}
            }
        )

    # Regra de Negócio (RN-005): Cancelamento exige justificativa
    if dados_update.status == StatusContratacao.CANCELADA and not dados_update.motivo_cancelamento:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "MISSING_CANCEL_REASON",
                "message": "O motivo do cancelamento é obrigatório ao cancelar uma contratação.",
                "details": None
            }
        )

    # Atualiza os dados principais
    contratacao.status = dados_update.status
    if dados_update.status == StatusContratacao.CANCELADA:
        contratacao.motivo_cancelamento = dados_update.motivo_cancelamento

    # Gera o registro na Tabela de Auditoria (Migration 3)
    auditoria = AuditoriaContratacao(
        contratacao_id=contratacao.id,
        status_anterior=status_atual.value,
        status_novo=dados_update.status.value
    )
    db.add(auditoria)
    db.commit()
    db.refresh(contratacao)

    return contratacao