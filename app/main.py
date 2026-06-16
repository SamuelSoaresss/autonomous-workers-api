from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import usuario, servico, contratacao, avaliacao

app = FastAPI(
    title="API Plataforma de Autônomos",
    description="API para gestão de trabalhadores autônomos e contratação de serviços.",
    version="1.0.0"
)



@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Se o erro já for um dicionário (como os que fizemos nas regras de negócio), repassa
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    
    # Se for uma string simples (como os erros padrão 404), formata para o nosso padrão
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "API_ERROR", "message": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extrai apenas os textos puros (campo e mensagem) para evitar crash de serialização
    erros_limpos = [{"campo": err.get("loc"), "mensagem": err.get("msg")} for err in exc.errors()]
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Os dados enviados são inválidos.",
            "details": erros_limpos
        }
    )



app.include_router(usuario.router)
app.include_router(servico.router)
app.include_router(contratacao.router)
app.include_router(avaliacao.router)

@app.get("/")
def read_root():
    return {"mensagem": "A API está no ar e o container subiu com sucesso!"}