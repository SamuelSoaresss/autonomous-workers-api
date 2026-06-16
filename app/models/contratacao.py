from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base

class StatusContratacao(str, enum.Enum):
    SOLICITADA = "SOLICITADA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"

class Contratacao(Base):
    __tablename__ = "contratacoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    servico_id = Column(UUID(as_uuid=True), ForeignKey("servicos.id"), nullable=False)
    
    valor_final = Column(Numeric(10, 2), nullable=False)
    data_agendada = Column(DateTime, nullable=False)
    status = Column(SQLEnum(StatusContratacao), default=StatusContratacao.SOLICITADA, nullable=False)
    
    # Nossa nova coluna para a Migration
    motivo_cancelamento = Column(String(255), nullable=True) 

    # Relacionamentos
    cliente = relationship("Usuario")
    servico = relationship("ServicoOferecido")