from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.connection import get_db
from app.models.user import User
from app.schemas.users import UserCreate, UserResponse
from app.services.security import gerar_hash
from app.api.auth import get_current_user

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

@router.get("/", response_model=List[UserResponse])
def listar_usuarios(
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    usuarios = db.query(User).all()

    return usuarios
@router.get("/{user_id}", response_model=UserResponse)
def buscar_usuario(
    user_id: int,
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    usuario = db.query(User).filter(
        User.id == user_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return usuario