from pydantic import BaseModel

class Cliente(BaseModel):
    id_: int | None = None
    nome: str
    email: str
    telefone: str