from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/login",
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "titulo": "Login - Techlog Soluction API",
            "descricao": "Página de login da Techlog Soluction API.",
        },
    )   

@router.post("/")
async def process_login(request: Request, email=Form(...), senha=Form(...)):
    if email == "admin@techlog.com.br" and senha == "admin123":
        response = RedirectResponse(url="/clientes", status_code=303)
        response.set_cookie(key="session_token", value="token-senha", httponly=True)
        return response

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "titulo": "Login - Techlog Soluction API",
            "descricao": "Página de login da Techlog Soluction API.",
            "error": "Credenciais inválidas. Tente novamente.",
        },
    )