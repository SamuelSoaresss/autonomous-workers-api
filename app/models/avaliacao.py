import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    # unique=True garante a relação 1 para 1 (uma contratação = uma avaliação)
    contratacao_id = Column(UUID(as_uuid=True), ForeignKey("contratacoes.id"), unique=True, nullable=False)
    
    nota = Column(Integer, nullable=False)
    comentario = Column(String, nullable=True)

    # Garante a regra de negócio direto no banco de dados
    __table_args__ = (
        CheckConstraint('nota >= 1 AND nota <= 5', name='check_nota_range'),
    )

    # Relacionamentos
    contratacao = relationship("Contratacao", backref="avaliacao")