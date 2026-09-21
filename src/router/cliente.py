from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.database.client_repository import ClientRepository
from src.dependencies import get_client_repository
from src.cliente import Cliente

router = APIRouter(
    prefix="/api/clientes",
)

front_router = APIRouter(
    prefix="/clientes",
)

templates = Jinja2Templates(directory="templates")

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

@front_router.get("/", response_class=HTMLResponse)
async def front_page(request: Request, cliente_repository: Annotated['ClientRepository', Depends(get_client_repository)]):
    clientes = await cliente_repository.list_client()
    return templates.TemplateResponse(
        request=request,
        name="clientes.html",
        context={
            "request": request,
            "clientes": clientes,
            "titulo": "Lista de Clientes",
            "descricao": "Esta é a lista de clientes cadastrados.",
        },
    )

@front_router.get("/novo", response_class=HTMLResponse)
async def front_new_client(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="clientes-form.html",
        context={
            "request": request,
            "titulo": "Novo Cliente",
            "descricao": "Formulário para cadastrar um novo cliente.",
        },
    )

@front_router.get("/{client_id}", response_class=HTMLResponse)
async def front_page_cliente(client_id: int, request: Request, cliente_repository: Annotated['ClientRepository', Depends(get_client_repository)]):
    cliente = await cliente_repository.get_client_by_id(client_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return templates.TemplateResponse(
        request=request,
        name="clientes-form.html",
        context={
            "request": request,
            "cliente": cliente,
            "titulo": f"Detalhes do Cliente {cliente.nome}",
            "descricao": f"Informações detalhadas sobre o cliente {cliente.nome}.",
        },
    )