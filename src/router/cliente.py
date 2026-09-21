from fastapi import APIRouter
from src.cliente import Cliente

router = APIRouter(
    prefix="/clientes",
)

@router.get("/", response_model=list[Cliente])
async def get_clientes():
    cliente_list = [
        Cliente(nome="João Silva", email="joao.silva@example.com", telefone="(11) 99999-9999"),
        Cliente(nome="Maria Souza", email="maria.souza@example.com", telefone="(11) 88888-8888"),
    ]
    return cliente_list