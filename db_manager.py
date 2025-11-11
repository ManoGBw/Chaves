# db_manager.py
import mysql.connector
from mysql.connector import errorcode
from db_config import DB_CONFIG

def get_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro: Verifique seu usuário ou senha do MySQL.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Erro: O banco de dados '{DB_CONFIG['database']}' não existe.")
        else:
            print(f"Erro ao conectar ao MySQL: {err}")
        return None

def execute_query(query, params=None):
    """Executa uma consulta (SELECT) e retorna todos os resultados."""
    conn = get_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor(dictionary=True) # dictionary=True retorna resultados como dicts
    try:
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as err:
        print(f"Erro na consulta: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def execute_commit(query, params=None):
    """Executa um comando de modificação (INSERT, UPDATE, DELETE) e faz commit."""
    conn = get_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        print("Operação realizada com sucesso.")
        return True
    except mysql.connector.Error as err:
        print(f"Erro na operação: {err}")
        conn.rollback() # Desfaz a operação em caso de erro
        return False
    finally:
        cursor.close()
        conn.close()