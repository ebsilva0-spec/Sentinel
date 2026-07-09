from app.database.connection import engine
from app.database.base import Base

# Importa os modelos para que o SQLAlchemy os conheça
from app.models.user import User

print("Criando tabelas...")

Base.metadata.create_all(bind=engine)

print("✅ Tabelas criadas com sucesso!")