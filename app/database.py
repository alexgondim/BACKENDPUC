# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:admin@localhost:3307/userdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base declarativa para os modelos herdar
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


def init_db():
    # Importa os modelos aqui para garantir que eles sejam conhecidos na hora da criação das tabelas
    # Por exemplo, assumindo que você tenha um módulo models com um modelo User dentro de app/models/user_model.py
    from app.models.user_model import User  # Importe todos os seus modelos aqui

    # Cria todas as tabelas no banco de dados
    # Este comando cria as tabelas se elas ainda não existem (com base nas definições dos modelos)
    Base.metadata.create_all(bind=engine)