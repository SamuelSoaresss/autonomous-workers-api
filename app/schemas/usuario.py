from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
import uuid

# Base com os campos comuns
class UsuarioBase(BaseModel):
    nome: str
    email: str
    is_worker: bool = False

    # Validador exigido na atividade (Pydantic v2)
    @field_validator('nome')
    @classmethod
    def validar_nome_vazio(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('O nome não pode ser vazio ou conter apenas espaços.')
        return value.strip()

    @field_validator('email')
    @classmethod
    def validar_formato_email(cls, value: str) -> str:
        if "@" not in value or "." not in value:
            raise ValueError('Formato de email inválido.')
        return value.lower().strip()

# Schema para criação (quando o cliente envia o POST)
class UsuarioCreate(UsuarioBase):
    pass

# Schema para retorno (quando a API devolve o JSON pro cliente)
class UsuarioResponse(UsuarioBase):
    id: uuid.UUID

    # Pydantic v2: permite ler dados direto do objeto SQLAlchemy
    model_config = ConfigDict(from_attributes=True)