from pydantic import BaseModel, ConfigDict
from decimal import Decimal
import uuid
from datetime import datetime
from typing import Optional

from app.models.contratacao import StatusContratacao

class ContratacaoBase(BaseModel):
    valor_final: Decimal
    data_agendada: datetime

class ContratacaoCreate(ContratacaoBase):
    cliente_id: uuid.UUID
    servico_id: uuid.UUID

class ContratacaoResponse(ContratacaoBase):
    id: uuid.UUID
    cliente_id: uuid.UUID
    servico_id: uuid.UUID
    status: StatusContratacao
    
    model_config = ConfigDict(from_attributes=True)

class ContratacaoStatusUpdate(BaseModel):
    status: StatusContratacao
    motivo_cancelamento: Optional[str] = None