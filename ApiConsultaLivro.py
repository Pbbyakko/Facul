from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, String, Boolean, DECIMAL
import os

# -------------------- Banco de Dados --------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("Variável de ambiente DATABASE_URL não configurada")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de tabela
class Livro(Base):
    __tablename__ = "livros"
    titulo = Column(String(200), primary_key=True)
    preco = Column(DECIMAL(15, 2))
    disponibilidade = Column(Boolean)
    avaliacao = Column(DECIMAL(10))
    pagina = Column(DECIMAL(10))

# -------------------- FastAPI App --------------------
app = FastAPI(
    title="API de Consulta de Livros",
    description="Serviço simples de consulta de livros",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/livros")
def listar_livros(db=Depends(get_db)):
    livros_tuplas = db.query(Livro.titulo, Livro.preco).all()
    
    # Converte tuplas para dicionários
    livros_dict = [
        {"titulo": titulo, "preco": float(preco) if preco else None}
        for titulo, preco in livros_tuplas
    ]
    
    return livros_dict

@app.get("/livro/{nome}")
def get_livro(nome: str, db=Depends(get_db)):
    livro = db.query(Livro).filter(Livro.titulo == nome).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    # Converte o objeto para dicionário
    return {
        "titulo": livro.titulo,
        "preco": float(livro.preco) if livro.preco else None,
        "disponibilidade": livro.disponibilidade,
        "avaliacao": float(livro.avaliacao) if livro.avaliacao else None,
        "pagina": float(livro.pagina) if livro.pagina else None
    }