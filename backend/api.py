from fastapi import FastAPI
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

# Criando a instância do FastAPI
app = FastAPI()

# Adicionando middleware para permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere para ["http://localhost:5173"] para mais segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota para pegar todas as vagas
@app.get("/vagas")
def get_vagas():
    conn = sqlite3.connect("vagas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT titulo, link FROM vagas")
    vagas = [{"titulo": row[0], "link": row[1]} for row in cursor.fetchall()]

    conn.close()
    return vagas
