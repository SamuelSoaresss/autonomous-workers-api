from sqlalchemy.orm import Session
from sqlalchemy import func
import uuid
from app.models.avaliacao import Avaliacao
from app.models.contratacao import Contratacao
from app.models.servico import ServicoOferecido
from app.schemas.avaliacao import AvaliacaoCreate

def criar_avaliacao(db: Session, avaliacao_in: AvaliacaoCreate):
    db_avaliacao = Avaliacao(**avaliacao_in.model_dump())
    db.add(db_avaliacao)
    db.commit()
    db.refresh(db_avaliacao)
    return db_avaliacao

def obter_media_trabalhador(db: Session, worker_id: uuid.UUID):
    # Faz um JOIN entre Avaliação, Contratação e Serviço para tirar a média das notas do trabalhador
    resultado = db.query(func.avg(Avaliacao.nota)).\
        join(Contratacao, Avaliacao.contratacao_id == Contratacao.id).\
        join(ServicoOferecido, Contratacao.servico_id == ServicoOferecido.id).\
        filter(ServicoOferecido.worker_id == worker_id).scalar()
    
    return round(float(resultado), 2) if resultado else 0.0