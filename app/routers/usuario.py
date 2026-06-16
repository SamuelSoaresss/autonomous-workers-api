from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.repositories import usuario as usuario_repo

# Cria um agrupador de rotas para organizar o Swagger
router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Envia os dados validados para o repositório salvar no banco
    return usuario_repo.criar_usuario(db=db, usuario_in=usuario)

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_repo.listar_usuarios(db=db)