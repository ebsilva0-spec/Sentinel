from datetime import datetime, timedelta, timezone

from jose import jwt

SECRET_KEY = "troque_essa_chave_por_uma_bem_grande_e_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def criar_access_token(data: dict):
    dados = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados.update({"exp": expire})

    return jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    )