import uuid
from sqlalchemy import Column, String, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class ServicoOferecido(Base):
    __tablename__ = "servicos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    worker_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    
    titulo = Column(String, nullable=False)
    preco_base = Column(Numeric(10, 2), nullable=False) # Permite valores como 99999999.99
    ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    worker = relationship("Usuario", backref="servicos_oferecidos")