from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from src.router import cliente as cliente_router

app = FastAPI(
    title="Techlog Soluction API - ALURA PROJECT",
    description="Projeto aula FAST API da Alura",
    version="0.0.1"
)

app.include_router(cliente_router.router)


@app.get("/health")
async def health():
    return {"status": "API is healthy"}

@app.get("/front", response_class=HTMLResponse)
async def front():
    html_content = """
    <html>
        <head>
            <title>Techlog Soluction</title>
        </head>
        <body>
            <h1>Bem-vindo à Techlog Soluction</h1>
            <p>Esta é a página inicial da API.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/jsontest", response_class=JSONResponse)
async def jsontest():
    json_content = {
        "message": "Esta é uma resposta JSON de teste.",
        "value": 42
    }
    return JSONResponse(content=json_content, status_code=201)

