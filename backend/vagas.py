import sqlite3
import os
db_path = os.path.abspath("vagas.db")
conn = sqlite3.connect(db_path)


# Conectar ao banco (cria se não existir)
conn = sqlite3.connect("vagas.db")
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS vagas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    link TEXT NOT NULL UNIQUE
)
""")

conn.commit()
conn.close()
