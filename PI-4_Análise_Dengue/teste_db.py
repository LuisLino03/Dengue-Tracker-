import sqlite3

conn = sqlite3.connect("ocorrencias.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("Tabelas no banco:", tabelas)

conn.close()
