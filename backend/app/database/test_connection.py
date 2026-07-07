from sqlalchemy import text

from app.database.connection import engine

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("✅ Conexão com o PostgreSQL realizada com sucesso!")

except Exception as e:
    print("❌ Erro ao conectar:")
    print(e)