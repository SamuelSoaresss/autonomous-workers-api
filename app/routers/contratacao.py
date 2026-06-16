from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.contratacao import ContratacaoCreate, ContratacaoResponse, ContratacaoStatusUpdate
from app.services import contratacao as contratacao_service

router = APIRouter(prefix="/contratacoes", tags=["Contratações"])

@router.post("/", response_model=ContratacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_contratacao(contratacao: ContratacaoCreate, db: Session = Depends(get_db)):
    # O router delega a criação para a camada de serviços
    return contratacao_service.criar_contratacao(db=db, contratacao_in=contratacao)

@router.patch("/{contratacao_id}/status", response_model=ContratacaoResponse)
def alterar_status(
    contratacao_id: str, 
    dados_update: ContratacaoStatusUpdate, 
    db: Session = Depends(get_db)
):
    # O router atua apenas como orquestrador, delegando a regra de transição de estado para o service
    return contratacao_service.atualizar_status_contratacao(
        db=db, 
        contratacao_id=contratacao_id, 
        dados_update=dados_update
    )