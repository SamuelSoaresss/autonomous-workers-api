from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.core.database import get_db
from app.models.usuario import Usuario
from app.models.servico import ServicoOferecido
from app.models.avaliacao import Avaliacao
from app.schemas.servico import ServicoCreate, ServicoResponse

router = APIRouter(prefix="/servicos", tags=["Servicos"])

@router.post("/{worker_id}", response_model=ServicoResponse, status_code=201)
def criar_servico(worker_id: str, servico: ServicoCreate, db: Session = Depends(get_db)):
    # Regra de Negócio (RN-001): Verifica se o usuário existe e se é um trabalhador (is_worker=True)
    usuario = db.query(Usuario).filter(Usuario.id == worker_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
    if not usuario.is_worker:
        # Retorna o erro no formato exigido pela atividade
        raise HTTPException(
            status_code=400, 
            detail={
                "error": "INVALID_WORKER_PROFILE",
                "message": "Apenas usuários 'worker' podem criar serviços.",
                "details": None
            }
        )
        
    novo_servico = ServicoOferecido(
        worker_id=worker_id,
        titulo=servico.titulo,
        preco_base=servico.preco_base,
        ativo=servico.ativo
    )
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)
    
    return novo_servico

@router.get("/", response_model=List[ServicoResponse])
def listar_servicos(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Paginação: itens a pular (offset)"),
    limit: int = Query(10, le=100, description="Paginação: limite máximo de itens"),
    titulo: Optional[str] = Query(None, description="Filtro opcional: buscar por parte do título")
):
    query = db.query(ServicoOferecido)
    
    # Aplica o filtro opcional se o usuário enviou o parâmetro na URL
    if titulo:
        query = query.filter(ServicoOferecido.titulo.ilike(f"%{titulo}%"))
        
    # Aplica a paginação (limit e offset) e retorna os resultados
    return query.offset(skip).limit(limit).all()

@router.get("/{servico_id}/media-avaliacoes")
def calcular_media_avaliacoes(servico_id: str, db: Session = Depends(get_db)):
    # Verifica se o serviço existe
    servico = db.query(ServicoOferecido).filter(ServicoOferecido.id == servico_id).first()
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    # Realiza o cálculo derivado (Média) diretamente no banco de dados usando func.avg
    resultado = db.query(func.avg(Avaliacao.nota)).filter(Avaliacao.servico_id == servico_id).scalar()
    
    # Se não houver avaliações, a média é 0.0
    media = round(resultado, 2) if resultado else 0.0
    total_avaliacoes = db.query(Avaliacao).filter(Avaliacao.servico_id == servico_id).count()
    
    return {
        "servico_id": servico_id,
        "titulo_servico": servico.titulo,
        "media_notas": media,
        "total_avaliacoes": total_avaliacoes
    }