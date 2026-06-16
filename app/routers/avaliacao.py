from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.core.database import get_db
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoResponse
from app.models.contratacao import Contratacao, StatusContratacao
from app.models.avaliacao import Avaliacao
from app.repositories import avaliacao_repo

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])

@router.post("/", response_model=AvaliacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_avaliacao(avaliacao: AvaliacaoCreate, db: Session = Depends(get_db)):
    contratacao = db.query(Contratacao).filter(Contratacao.id == avaliacao.contratacao_id).first()
    if not contratacao:
        raise HTTPException(status_code=404, detail="Contratação não encontrada.")

    # RN-002: Avaliação exige conclusão de serviço
    if contratacao.status != StatusContratacao.CONCLUIDA:
        raise HTTPException(
            status_code=422,
            detail={"error": "SERVICE_NOT_COMPLETED", "message": "O serviço precisa estar concluído antes de receber uma avaliação."}
        )

    # RN-005: Prevenção de dupla avaliação
    avaliacao_existente = db.query(Avaliacao).filter(Avaliacao.contratacao_id == avaliacao.contratacao_id).first()
    if avaliacao_existente:
        raise HTTPException(
            status_code=409,
            detail={"error": "DUPLICATE_REVIEW", "message": "Este serviço já foi avaliado anteriormente."}
        )

    return avaliacao_repo.criar_avaliacao(db=db, avaliacao_in=avaliacao)

@router.get("/trabalhador/{worker_id}/media")
def obter_media(worker_id: uuid.UUID, db: Session = Depends(get_db)):
    media = avaliacao_repo.obter_media_trabalhador(db=db, worker_id=worker_id)
    return {"worker_id": worker_id, "nota_media": media}