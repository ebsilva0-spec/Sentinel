from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.users import TokenResponse
from app.services.security import verificar_senha
from app.core.security import (
    criar_access_token,
    verificar_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


@router.post("/login", response_model=TokenResponse)
def login(
    dados: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(User).filter(
        User.email == dados.username
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    if not verificar_senha(
        dados.password,
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


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    email = verificar_access_token(token)
    return email


@router.get("/me")
def me(
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    usuario = db.query(User).filter(
        User.email == email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email
    }