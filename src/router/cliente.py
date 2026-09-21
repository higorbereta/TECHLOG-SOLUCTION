from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from src.database.client_repository import ClientRepository
from src.dependencies import get_client_repository
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

@router.post("/", response_model=Cliente, status_code=201)
async def create_cliente(cliente: Cliente, client_repository: Annotated['ClientRepository', Depends(get_client_repository)]):
    return await client_repository.create_client(cliente)

@router.put("/{client_id}", response_model=Cliente | None)
async def update_cliente(client_id: int, cliente: Cliente, client_repository: Annotated['ClientRepository', Depends(get_client_repository)]):
    cliente.id_ = client_id
    updated_cliente = await client_repository.update_client(cliente)

    if not updated_cliente:
        return HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return updated_cliente

@router.delete("/{client_id}", status_code=204)
async def delete_cliente(client_id: int, client_repository: Annotated['ClientRepository', Depends(get_client_repository)]):
    deleted = await client_repository.delete_client(client_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return None