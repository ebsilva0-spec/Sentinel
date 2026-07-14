from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.users import LoginRequest, TokenResponse
from app.services.security import verificar_senha
from app.core.security import criar_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=TokenResponse)
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):
    usuario = db.query(User).filter(
        User.email == dados.email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    if not verificar_senha(
        dados.senha,
        usuario.senha
    ):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    token = criar_access_token(
        data={"sub": usuario.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }