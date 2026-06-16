from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.models.servico import ServicoOferecido
from app.schemas.servico import ServicoCreate

def criar_servico(db: Session, servico_in: ServicoCreate, worker_id: str):
    db_servico = ServicoOferecido(**servico_in.model_dump(), worker_id=worker_id)
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico

def listar_servicos(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    preco_max: Optional[float] = None, 
    termo_busca: Optional[str] = None
):
    query = db.query(ServicoOferecido).filter(ServicoOferecido.ativo == True)
    
    # Filtro opcional por termo de busca no título (case-insensitive)
    if termo_busca:
        query = query.filter(func.lower(ServicoOferecido.titulo).contains(termo_busca.lower()))
        
    # Filtro opcional por preço máximo
    if preco_max is not None:
        query = query.filter(ServicoOferecido.preco_base <= preco_max)
        
    # Aplica a paginação (skip pula registros, limit dita o tamanho da página)
    return query.offset(skip).limit(limit).all()