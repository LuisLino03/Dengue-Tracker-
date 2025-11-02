import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='ocorrencias.db'):
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ocorrencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                -- Campos epidemiológicos (agora primeiro)
                sinan TEXT,
                data_notificacao TEXT,
                inicio_sintoma TEXT,
                data_exame TEXT,
                tipo_exame TEXT,
                resultado TEXT,
                tipo_doenca TEXT,
                classificacao TEXT,
                data_resultado TEXT,
                cc TEXT,
                np TEXT,
                sinais_alerta TEXT,
                
                -- Dados pessoais
                nome TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                logradouro TEXT NOT NULL,
                numero TEXT NOT NULL,
                bairro TEXT NOT NULL,
                quarterao TEXT NOT NULL,
                
                data_criacao TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def inserir_ocorrencia(self, sinan, data_notificacao, inicio_sintoma, data_exame, tipo_exame, resultado,
                          tipo_doenca, classificacao, data_resultado, cc, np, sinais_alerta,
                          nome, data_nascimento, logradouro, numero, bairro, quarterao):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO ocorrencias 
            (sinan, data_notificacao, inicio_sintoma, data_exame, tipo_exame, resultado,
             tipo_doenca, classificacao, data_resultado, cc, np, sinais_alerta,
             nome, data_nascimento, logradouro, numero, bairro, quarterao, data_criacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sinan, data_notificacao, inicio_sintoma, data_exame, tipo_exame, resultado,
              tipo_doenca, classificacao, data_resultado, cc, np, sinais_alerta,
              nome, data_nascimento, logradouro, numero, bairro, quarterao, data_criacao))
        
        conn.commit()
        conn.close()
        return True
    
    def buscar_ocorrencias(self, filtro=None, valor=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        if filtro and valor:
            if filtro == "nome":
                cursor.execute('SELECT * FROM ocorrencias WHERE nome LIKE ? ORDER BY data_criacao DESC', (f'%{valor}%',))
            elif filtro == "bairro":
                cursor.execute('SELECT * FROM ocorrencias WHERE bairro LIKE ? ORDER BY data_criacao DESC', (f'%{valor}%',))
            elif filtro == "quarterao":
                cursor.execute('SELECT * FROM ocorrencias WHERE quarterao LIKE ? ORDER BY data_criacao DESC', (f'%{valor}%',))
            elif filtro == "sinan":
                cursor.execute('SELECT * FROM ocorrencias WHERE sinan LIKE ? ORDER BY data_criacao DESC', (f'%{valor}%',))
            else:
                cursor.execute('SELECT * FROM ocorrencias ORDER BY data_criacao DESC')
        else:
            cursor.execute('SELECT * FROM ocorrencias ORDER BY data_criacao DESC')
            
        ocorrencias = cursor.fetchall()
        
        conn.close()
        return ocorrencias
    
    def buscar_ocorrencia_por_id(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM ocorrencias WHERE id = ?', (id,))
        ocorrencia = cursor.fetchone()
        
        conn.close()
        return ocorrencia
    
    def atualizar_ocorrencia(self, id, sinan, data_notificacao, inicio_sintoma, data_exame, tipo_exame, resultado,
                           tipo_doenca, classificacao, data_resultado, cc, np, sinais_alerta,
                           nome, data_nascimento, logradouro, numero, bairro, quarterao):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE ocorrencias 
            SET sinan = ?, data_notificacao = ?, inicio_sintoma = ?, data_exame = ?, tipo_exame = ?, resultado = ?,
                tipo_doenca = ?, classificacao = ?, data_resultado = ?, cc = ?, np = ?, sinais_alerta = ?,
                nome = ?, data_nascimento = ?, logradouro = ?, numero = ?, bairro = ?, quarterao = ?
            WHERE id = ?
        ''', (sinan, data_notificacao, inicio_sintoma, data_exame, tipo_exame, resultado,
              tipo_doenca, classificacao, data_resultado, cc, np, sinais_alerta,
              nome, data_nascimento, logradouro, numero, bairro, quarterao, id))
        
        conn.commit()
        conn.close()
        return True
    
    def excluir_ocorrencia(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM ocorrencias WHERE id = ?', (id,))
        
        conn.commit()
        conn.close()
        return True