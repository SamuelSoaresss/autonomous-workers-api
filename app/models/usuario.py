import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    # UUID como chave primária obrigatória
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Atributos obrigatórios
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Define se é um cliente comum ou um trabalhador autônomo
    is_worker = Column(Boolean, default=False, nullable=False)