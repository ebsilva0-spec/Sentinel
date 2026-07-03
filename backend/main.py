from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "mensagem": "Bem-vindo ao Sentinel!",
        "versao": "1.0.0"
    }   
