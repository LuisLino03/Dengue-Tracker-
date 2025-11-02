import sqlite3
import os

# Caminho do banco
DB_PATH = "ocorrencias.db"

# -------------------- APAGAR BANCO ANTIGO --------------------
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("Banco antigo apagado.")

# -------------------- CRIAR NOVO BANCO E TABELA --------------------
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Criação da tabela de ocorrências
cursor.execute("""
CREATE TABLE ocorrencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sinan TEXT,
    data_notificacao DATE,
    inicio_sintoma DATE,
    data_exame DATE,
    tipo_exame TEXT,
    resultado TEXT,
    tipo_doenca TEXT,
    classificacao TEXT,
    data_resultado DATE,
    cc TEXT,
    np TEXT,
    sinais_alerta TEXT,
    nome TEXT,
    data_nascimento DATE,
    logradouro TEXT,
    numero TEXT,
    bairro TEXT,
    quarterao TEXT,
    data_criacao DATE
)
""")

conn.commit()
conn.close()
print("Banco criado e pronto para novos testes!")
