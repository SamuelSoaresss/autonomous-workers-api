from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
import uuid

class AvaliacaoBase(BaseModel):
    nota: int
    comentario: Optional[str] = None

    @field_validator('nota')
    @classmethod
    def validar_nota(cls, value: int) -> int:
        if value < 1 or value > 5:
            raise ValueError('A nota deve ser um número inteiro entre 1 e 5.')
        return value

class AvaliacaoCreate(AvaliacaoBase):
    contratacao_id: uuid.UUID

class AvaliacaoResponse(AvaliacaoBase):
    id: uuid.UUID
    contratacao_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)