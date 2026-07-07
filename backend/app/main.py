from fastapi import FastAPI

from app.api.health import router as health_router

app = FastAPI(
    title="Sentinel API",
    description="API desenvolvida por Edson Barbosa.",
    version="1.0.0"
)

app.include_router(health_router)

@app.get("/")
def home():
    return {
        "mensagem": "Bem-vindo à Sentinel API!",
        "status": "online"
    }