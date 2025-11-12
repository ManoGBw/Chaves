import db_manager
from datetime import datetime
import mysql.connector 

def verificar_chaves_disponiveis():
    print("\n--- Chaves Disponíveis ---")
    query = """
    SELECT 
        c.codigo_visual, 
        s.numero_sala, 
        b.nome_bloco
    FROM CHAVE c
    JOIN SALA s ON c.id_sala = s.id_sala
    JOIN BLOCO b ON s.id_bloco = b.id_bloco
    WHERE s.status = 'Disponível'
    """
    
    chaves = db_manager.execute_query(query)
    
    if not chaves:
        print("Nenhuma chave disponível no momento.")
        return

    for chave in chaves:
        print(f"Bloco: {chave['nome_bloco']} | Sala: {chave['numero_sala']} | Código: {chave['codigo_visual']}")

def realizar_emprestimo(cpf_pessoa, codigo_chave, id_funcionario_retirada):
    print(f"\nTentando empréstimo da chave {codigo_chave} para o CPF {cpf_pessoa}...")

    conn = db_manager.get_connection()
    if conn is None:
        return
    
    cursor = conn.cursor(buffered=True)

    try:
        query_verificacao = """
        SELECT 
            c.id_chave, 
            s.id_sala,
            s.status
        FROM CHAVE c
        JOIN SALA s ON c.id_sala = s.id_sala
        WHERE c.codigo_visual = %s
        """
        cursor.execute(query_verificacao, (codigo_chave,))
        chave_info = cursor.fetchone()

        if not chave_info:
            print(f"Erro: Chave com código '{codigo_chave}' não encontrada.")
            raise Exception("Chave não encontrada")

        (id_chave, id_sala, status) = chave_info
        
        if status != 'Disponível':
            print(f"Erro: A sala desta chave ('{status}') não está disponível.")
            raise Exception("Sala não disponível")

        cursor.execute("SELECT cpf FROM PESSOA WHERE cpf = %s", (cpf_pessoa,))
        if not cursor.fetchone():
            print(f"Erro: Pessoa com CPF '{cpf_pessoa}' não encontrada.")
            raise Exception("Pessoa não encontrada")

        cursor.execute("SELECT id_funcionario FROM FUNCIONARIO WHERE id_funcionario = %s", (id_funcionario_retirada,))
        if not cursor.fetchone():
            print(f"Erro: Funcionário com ID '{id_funcionario_retirada}' não encontrado.")
            raise Exception("Funcionário não encontrado")

        query_insert = """
        INSERT INTO EMPRESTIMO 
            (id_chave, cpf_pessoa, id_funcionario_retirada, data_hora_retirada, data_hora_devolucao)
        VALUES (%s, %s, %s, %s, NULL)
        """
        data_agora = datetime.now()
        cursor.execute(query_insert, (id_chave, cpf_pessoa, id_funcionario_retirada, data_agora))

        query_update = "UPDATE SALA SET status = 'Indisponível' WHERE id_sala = %s"
        cursor.execute(query_update, (id_sala,))

        conn.commit()
        print("Empréstimo realizado com sucesso!")

    except Exception as e:
        print(f"Falha na operação: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()


def realizar_devolucao(codigo_chave, id_funcionario_devolucao):
    print(f"\nTentando devolução da chave {codigo_chave}...")

    conn = db_manager.get_connection()
    if conn is None:
        return
    cursor = conn.cursor(buffered=True)

    try:
        query_busca = """
        SELECT h.id_emprestimo, c.id_chave, s.id_sala
        FROM EMPRESTIMO h
        JOIN CHAVE c ON h.id_chave = c.id_chave
        JOIN SALA s ON c.id_sala = s.id_sala
        WHERE c.codigo_visual = %s AND h.data_hora_devolucao IS NULL
        """
        cursor.execute(query_busca, (codigo_chave,))
        emprestimo_info = cursor.fetchone()

        if not emprestimo_info:
            print(f"Erro: Não há empréstimo ativo para a chave '{codigo_chave}'.")
            raise Exception("Empréstimo não encontrado")
        
        (id_emprestimo, id_chave, id_sala) = emprestimo_info

        cursor.execute("SELECT id_funcionario FROM FUNCIONARIO WHERE id_funcionario = %s", (id_funcionario_devolucao,))
        if not cursor.fetchone():
            print(f"Erro: Funcionário com ID '{id_funcionario_devolucao}' não encontrado.")
            raise Exception("Funcionário não encontrado")

        query_update_hist = """
        UPDATE EMPRESTIMO
        SET data_hora_devolucao = %s, id_funcionario_devolucao = %s
        WHERE id_emprestimo = %s
        """
        data_agora = datetime.now()
        cursor.execute(query_update_hist, (data_agora, id_funcionario_devolucao, id_emprestimo))

        query_update_sala = "UPDATE SALA SET status = 'Disponível' WHERE id_sala = %s"
        cursor.execute(query_update_sala, (id_sala,))

        conn.commit()
        print("Devolução realizada com sucesso!")

    except Exception as e:
        print(f"Falha na operação: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()


def cadastrar_aluno(cpf, nome, telefone, matricula):
    conn = db_manager.get_connection()
    if conn is None:
        return
        
    cursor = conn.cursor(buffered=True)
    try:
        query_pessoa = "INSERT INTO PESSOA (cpf, nome, telefone) VALUES (%s, %s, %s)"
        cursor.execute(query_pessoa, (cpf, nome, telefone))
        
        query_aluno = "INSERT INTO ALUNO (cpf, numero_matricula) VALUES (%s, %s)"
        cursor.execute(query_aluno, (cpf, matricula))

        conn.commit()
        print(f"Aluno {nome} (CPF: {cpf}) cadastrado com sucesso.")
    
    except mysql.connector.Error as err:
        if err.errno == 1062: # Duplicate entry
            print(f"Erro: O CPF '{cpf}' ou a Matrícula '{matricula}' já existem no banco.")
        else:
            print(f"Erro ao cadastrar aluno: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def cadastrar_professor(cpf, nome, telefone, siape, departamento):
    conn = db_manager.get_connection()
    if conn is None:
        return
        
    cursor = conn.cursor(buffered=True)
    try:
        query_pessoa = "INSERT INTO PESSOA (cpf, nome, telefone) VALUES (%s, %s, %s)"
        cursor.execute(query_pessoa, (cpf, nome, telefone))
        
        query_prof = "INSERT INTO PROFESSOR (cpf, siape, departamento) VALUES (%s, %s, %s)"
        cursor.execute(query_prof, (cpf, siape, departamento))

        conn.commit()
        print(f"Professor {nome} (CPF: {cpf}) cadastrado com sucesso.")
    
    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar professor: {err}")
        if err.errno == 1062: # Duplicate entry
            print("Erro: O CPF ou o SIAPE informados já existem.")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def cadastrar_servidor_tecnico(cpf, nome, telefone, siape, setor):
    conn = db_manager.get_connection()
    if conn is None:
        return
        
    cursor = conn.cursor(buffered=True)
    try:
        query_pessoa = "INSERT INTO PESSOA (cpf, nome, telefone) VALUES (%s, %s, %s)"
        cursor.execute(query_pessoa, (cpf, nome, telefone))
        
        query_serv = "INSERT INTO SERVIDOR_TECNICO (cpf, siape, setor) VALUES (%s, %s, %s)"
        cursor.execute(query_serv, (cpf, siape, setor))

        conn.commit()
        print(f"Servidor {nome} (CPF: {cpf}) cadastrado com sucesso.")
    
    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar servidor: {err}")
        if err.errno == 1062: # Duplicate entry
            print("Erro: O CPF ou o SIAPE informados já existem.")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def listar_blocos():
    print("\n--- Blocos Disponíveis ---")
    query = "SELECT id_bloco, nome_bloco FROM BLOCO"
    blocos = db_manager.execute_query(query)
    
    if not blocos:
        print("Atenção: Nenhum bloco cadastrado.")
        print("Você precisa cadastrar um BLOCO no banco antes de criar salas.")
        return False

    for bloco in blocos:
        print(f"ID: {bloco['id_bloco']} | Nome: {bloco['nome_bloco']}")
    return True

def cadastrar_sala_de_aula(numero_sala, id_bloco, capacidade, codigo_visual):
    """Cadastra SALA, SALA_DE_AULA e CHAVE (em uma transação)."""
    conn = db_manager.get_connection()
    if conn is None:
        return
    cursor = conn.cursor(buffered=True)
    
    try:
        query_sala = """
        INSERT INTO SALA (numero_sala, status, id_bloco) 
        VALUES (%s, 'Disponível', %s)
        """
        cursor.execute(query_sala, (numero_sala, id_bloco))
        
        id_sala_gerado = cursor.lastrowid

        query_tipo = """
        INSERT INTO SALA_DE_AULA (id_sala, capacidade_alunos) 
        VALUES (%s, %s)
        """
        cursor.execute(query_tipo, (id_sala_gerado, capacidade))

        query_chave = """
        INSERT INTO CHAVE (codigo_visual, id_sala) 
        VALUES (%s, %s)
        """
        cursor.execute(query_chave, (codigo_visual, id_sala_gerado))

        conn.commit()
        print(f"Sala de Aula '{numero_sala}' (ID: {id_sala_gerado}) e Chave '{codigo_visual}' cadastradas com sucesso.")

    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar Sala de Aula: {err}")
        if err.errno == 1062: 
            print("Erro: O Código Visual da Chave já existe ou a Sala já possui uma chave.")
        elif err.errno == 1452: 
            print(f"Erro: O Bloco com ID '{id_bloco}' não existe.")
        conn.rollback() 
    finally:
        cursor.close()
        conn.close()

def cadastrar_laboratorio(numero_sala, id_bloco, qtde_computadores, codigo_visual):
    """Cadastra SALA, LABORATORIO e CHAVE (em uma transação)."""
    conn = db_manager.get_connection()
    if conn is None:
        return
    cursor = conn.cursor(buffered=True)
    
    try:
        query_sala = """
        INSERT INTO SALA (numero_sala, status, id_bloco) 
        VALUES (%s, 'Disponível', %s)
        """
        cursor.execute(query_sala, (numero_sala, id_bloco))
        
        id_sala_gerado = cursor.lastrowid

        query_tipo = """
        INSERT INTO LABORATORIO (id_sala, qtde_computadores) 
        VALUES (%s, %s)
        """
        cursor.execute(query_tipo, (id_sala_gerado, qtde_computadores))

        query_chave = """
        INSERT INTO CHAVE (codigo_visual, id_sala) 
        VALUES (%s, %s)
        """
        cursor.execute(query_chave, (codigo_visual, id_sala_gerado))

        conn.commit()
        print(f"Laboratório '{numero_sala}' (ID: {id_sala_gerado}) e Chave '{codigo_visual}' cadastrados com sucesso.")

    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar Laboratório: {err}")
        if err.errno == 1062:
            print("Erro: O Código Visual da Chave já existe ou a Sala já possui uma chave.")
        elif err.errno == 1452:
            print(f"Erro: O Bloco com ID '{id_bloco}' não existe.")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def cadastrar_escritorio(numero_sala, id_bloco, setor_responsavel, codigo_visual):
    """Cadastra SALA, ESCRITORIO e CHAVE (em uma transação)."""
    conn = db_manager.get_connection()
    if conn is None:
        return
    cursor = conn.cursor(buffered=True)
    
    try:
        query_sala = """
        INSERT INTO SALA (numero_sala, status, id_bloco) 
        VALUES (%s, 'Disponível', %s)
        """
        cursor.execute(query_sala, (numero_sala, id_bloco))

        id_sala_gerado = cursor.lastrowid
        
        query_tipo = """
        INSERT INTO ESCRITORIO (id_sala, setor_responsavel) 
        VALUES (%s, %s)
        """
        cursor.execute(query_tipo, (id_sala_gerado, setor_responsavel))

        query_chave = """
        INSERT INTO CHAVE (codigo_visual, id_sala) 
        VALUES (%s, %s)
        """
        cursor.execute(query_chave, (codigo_visual, id_sala_gerado))

        conn.commit()
        print(f"Escritório '{numero_sala}' (ID: {id_sala_gerado}) e Chave '{codigo_visual}' cadastrados com sucesso.")

    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar Escritório: {err}")
        if err.errno == 1062:
            print("Erro: O Código Visual da Chave já existe ou a Sala já possui uma chave.")
        elif err.errno == 1452:
            print(f"Erro: O Bloco com ID '{id_bloco}' não existe.")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()