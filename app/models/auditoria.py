from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.core.database import Base

class AuditoriaContratacao(Base):
    __tablename__ = "auditoria_contratacoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contratacao_id = Column(UUID(as_uuid=True), ForeignKey("contratacoes.id", ondelete="CASCADE"), nullable=False)
    status_anterior = Column(String(50), nullable=True)
    status_novo = Column(String(50), nullable=False)
    data_alteracao = Column(DateTime, default=datetime.utcnow, nullable=False)