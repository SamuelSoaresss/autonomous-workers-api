from pydantic import BaseModel, ConfigDict, field_validator
from decimal import Decimal
from typing import Optional
import uuid

class ServicoBase(BaseModel):
    titulo: str
    preco_base: Decimal
    descricao: Optional[str] = None
    ativo: bool = True

    @field_validator('titulo')
    @classmethod
    def validar_titulo(cls, value: str) -> str:
        if len(value) < 5:
            raise ValueError('O título do serviço deve ter pelo menos 5 caracteres.')
        return value.strip()

    @field_validator('preco_base')
    @classmethod
    def validar_preco(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError('O preço base do serviço deve ser maior que zero.')
        return value

class ServicoCreate(ServicoBase):
    pass

class ServicoResponse(ServicoBase):
    id: uuid.UUID
    worker_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)