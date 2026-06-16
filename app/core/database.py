import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Pega a URL do banco do ambiente (que o Docker injeta usando o .env)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:adminpassword@localhost:5433/worker_platform"
)

# Cria o motor de conexão com o PostgreSQL
engine = create_engine(DATABASE_URL)

# Cria a fábrica de sessões para conversarmos com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para criarmos nossos modelos
Base = declarative_base()

# Dependência do FastAPI para injetar a sessão do banco nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()