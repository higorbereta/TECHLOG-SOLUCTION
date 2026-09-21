from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from src.router import cliente as cliente_router

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="Techlog Soluction API - ALURA PROJECT",
    description="Projeto aula FAST API da Alura",
    version="0.0.1"
)

app.include_router(cliente_router.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
async def health():
    return {"status": "API is healthy"}

@app.get("/", response_class=HTMLResponse)
async def front_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "titulo": "Techlog Soluction API - ALURA PROJECT",
            "descricao": "Projeto aula FAST API da Alura",
            "versao": "0.0.1",
        },
    )

@app.get("/jsontest", response_class=JSONResponse)
async def jsontest():
    json_content = {
        "message": "Esta é uma resposta JSON de teste.",
        "value": 42
    }
    return JSONResponse(content=json_content, status_code=201)

