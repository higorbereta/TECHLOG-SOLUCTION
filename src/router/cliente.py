from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from database.client_repository import ClientRepository
from dependencies import get_client_repository
from src.cliente import Cliente

router = APIRouter(
    prefix="/clientes",
)

@router.get("/", response_model=list[Cliente])
async def get_clientes(client_repository: Annotated['ClientRepository', Depends(get_client_repository)]):
    return await client_repository.list_client()

@router.get("/{client_id}", response_model=Cliente | None)
async def get_cliente_by_id(client_id: int, client_repository: Annotated['ClientRepository', Depends(get_client_repository)]):
    cliente = await client_repository.get_client_by_id(client_id)

    if not cliente:
        return HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return cliente