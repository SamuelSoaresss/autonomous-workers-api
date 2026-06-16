from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate

def criar_usuario(db: Session, usuario_in: UsuarioCreate):
    # Converte o schema do Pydantic em um modelo do SQLAlchemy
    db_usuario = Usuario(**usuario_in.model_dump())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def listar_usuarios(db: Session):
    return db.query(Usuario).all()