from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.connection import get_db
from app.models.user import User
from app.schemas.users import UserCreate, UserResponse
from app.services.security import gerar_hash

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def criar_usuario(
    usuario: UserCreate,
    db: Session = Depends(get_db)
):
    novo_usuario = User(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash(usuario.senha)
    )

    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="E-mail já cadastrado."
        )

    return novo_usuario