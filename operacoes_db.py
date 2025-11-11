import db_manager
from datetime import datetime
import mysql.connector 

def verificar_chaves_disponiveis():
    """Consulta e exibe todas as chaves com status 'Disponível'."""
    
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
    """
    Realiza o empréstimo de uma chave.
    Isso requer uma TRANSAÇÃO.
    """
    print(f"\nTentando empréstimo da chave {codigo_chave} para o CPF {cpf_pessoa}...")

    conn = db_manager.get_connection()
    if conn is None:
        return
    
    cursor = conn.cursor()

    try:
        # 1. Verificar chave e pegar IDs
        # <-- MUDANÇA: Query ajustada para CHAVE e SALA
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

        # 2. Verificar se a Pessoa (CPF) existe
        # <-- MUDANÇA: Usamos PESSOA e verificamos o CPF
        cursor.execute("SELECT cpf FROM PESSOA WHERE cpf = %s", (cpf_pessoa,))
        if not cursor.fetchone():
            print(f"Erro: Pessoa com CPF '{cpf_pessoa}' não encontrada.")
            raise Exception("Pessoa não encontrada")
        # Não precisamos de id_pessoa, o próprio CPF será usado

        # 3. Verificar se o Funcionário (ID) existe
        # <-- MUDANÇA: Usamos FUNCIONARIO e verificamos o id_funcionario
        cursor.execute("SELECT id_funcionario FROM FUNCIONARIO WHERE id_funcionario = %s", (id_funcionario_retirada,))
        if not cursor.fetchone():
            print(f"Erro: Funcionário com ID '{id_funcionario_retirada}' não encontrado.")
            raise Exception("Funcionário não encontrado")

        # 4. Inserir no EMPRESTIMO
        # <-- MUDANÇA: Tabela 'EMPRESTIMO' e colunas corretas
        query_insert = """
        INSERT INTO EMPRESTIMO 
            (id_chave, cpf_pessoa, id_funcionario_retirada, data_hora_retirada, data_hora_devolucao)
        VALUES (%s, %s, %s, %s, NULL)
        """
        data_agora = datetime.now()
        # Note a ordem dos parâmetros: id_chave, cpf_pessoa, id_funcionario_retirada
        cursor.execute(query_insert, (id_chave, cpf_pessoa, id_funcionario_retirada, data_agora))

        # 5. Atualizar status da Sala
        # <-- MUDANÇA: Tabela 'SALA'
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
    """
    Realiza a devolução de uma chave.
    Outra TRANSAÇÃO.
    """
    print(f"\nTentando devolução da chave {codigo_chave}...")

    conn = db_manager.get_connection()
    if conn is None:
        return
    cursor = conn.cursor()

    try:
        # 1. Encontrar o empréstimo ativo e IDs
        # <-- MUDANÇA: Query ajustada para EMPRESTIMO, CHAVE, SALA e colunas
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

        # 2. Verificar ID do Funcionário
        # <-- MUDANÇA: Usamos FUNCIONARIO
        cursor.execute("SELECT id_funcionario FROM FUNCIONARIO WHERE id_funcionario = %s", (id_funcionario_devolucao,))
        if not cursor.fetchone():
            print(f"Erro: Funcionário com ID '{id_funcionario_devolucao}' não encontrado.")
            raise Exception("Funcionário não encontrado")

        # 3. Atualizar o EMPRESTIMO
        # <-- MUDANÇA: Tabela 'EMPRESTIMO' e colunas corretas
        query_update_hist = """
        UPDATE EMPRESTIMO
        SET data_hora_devolucao = %s, id_funcionario_devolucao = %s
        WHERE id_emprestimo = %s
        """
        data_agora = datetime.now()
        cursor.execute(query_update_hist, (data_agora, id_funcionario_devolucao, id_emprestimo))

        # 4. Atualizar o status da Sala
        # <-- MUDANÇA: Tabela 'SALA'
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


#
# Exemplo de cadastro de Aluno (que é uma Pessoa)
# Esta é a lógica correta para o seu esquema (Pessoa -> Aluno)
#
def cadastrar_aluno(cpf, nome, telefone, matricula):
    """Cadastra uma nova pessoa e, em seguida, um aluno (em uma transação)."""
    conn = db_manager.get_connection()
    if conn is None:
        return
        
    cursor = conn.cursor()
    try:
        # 1. Insere na tabela 'Pai' (PESSOA)
        query_pessoa = "INSERT INTO PESSOA (cpf, nome, telefone) VALUES (%s, %s, %s)"
        cursor.execute(query_pessoa, (cpf, nome, telefone))
        
        # 2. Insere na tabela 'Filha' (ALUNO)
        #    Usa o mesmo CPF que é a chave primária e estrangeira
        query_aluno = "INSERT INTO ALUNO (cpf, numero_matricula) VALUES (%s, %s)"
        cursor.execute(query_aluno, (cpf, matricula))

        conn.commit()
        print(f"Aluno {nome} (CPF: {cpf}) cadastrado com sucesso.")
    
    except mysql.connector.Error as err:
        # Trata erros comuns, como CPF duplicado
        if err.errno == 1062: # Duplicate entry
            print(f"Erro: O CPF '{cpf}' ou a Matrícula '{matricula}' já existem no banco.")
        else:
            print(f"Erro ao cadastrar aluno: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def cadastrar_aluno(cpf, nome, telefone, matricula):
    """Cadastra uma nova pessoa e, em seguida, um aluno (em uma transação)."""
    conn = db_manager.get_connection()
    if conn is None:
        return
        
    cursor = conn.cursor()
    try:
        # 1. Insere na tabela 'Pai' (PESSOA)
        query_pessoa = "INSERT INTO PESSOA (cpf, nome, telefone) VALUES (%s, %s, %s)"
        cursor.execute(query_pessoa, (cpf, nome, telefone))
        
        # 2. Insere na tabela 'Filha' (ALUNO)
        query_aluno = "INSERT INTO ALUNO (cpf, numero_matricula) VALUES (%s, %s)"
        cursor.execute(query_aluno, (cpf, matricula))

        # Se ambos os inserts deram certo, confirma a transação
        conn.commit()
        print(f"Aluno {nome} (CPF: {cpf}) cadastrado com sucesso.")
    
    except mysql.connector.Error as err:
        # Se algo deu errado (ex: CPF duplicado), desfaz tudo
        print(f"Erro ao cadastrar aluno: {err}")
        if err.errno == 1062: # Duplicate entry
            print("Erro: O CPF ou a Matrícula informados já existem.")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def cadastrar_professor(cpf, nome, telefone, siape, departamento):
    """Cadastra uma nova pessoa e, em seguida, um professor (em uma transação)."""
    conn = db_manager.get_connection()
    if conn is None:
        return
        
    cursor = conn.cursor()
    try:
        # 1. Insere na tabela 'Pai' (PESSOA)
        query_pessoa = "INSERT INTO PESSOA (cpf, nome, telefone) VALUES (%s, %s, %s)"
        cursor.execute(query_pessoa, (cpf, nome, telefone))
        
        # 2. Insere na tabela 'Filha' (PROFESSOR)
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
    """Cadastra uma nova pessoa e, em seguida, um servidor (em uma transação)."""
    conn = db_manager.get_connection()
    if conn is None:
        return
        
    cursor = conn.cursor()
    try:
        # 1. Insere na tabela 'Pai' (PESSOA)
        query_pessoa = "INSERT INTO PESSOA (cpf, nome, telefone) VALUES (%s, %s, %s)"
        cursor.execute(query_pessoa, (cpf, nome, telefone))
        
        # 2. Insere na tabela 'Filha' (SERVIDOR_TECNICO)
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
    """Consulta e exibe os blocos cadastrados."""
    print("\n--- Blocos Disponíveis ---")
    query = "SELECT id_bloco, nome_bloco FROM BLOCO"
    blocos = db_manager.execute_query(query)
    
    if not blocos:
        print("Atenção: Nenhum bloco cadastrado.")
        print("Você precisa cadastrar um BLOCO no banco antes de criar salas.")
        return False # Retorna False para indicar que não há blocos

    for bloco in blocos:
        print(f"ID: {bloco['id_bloco']} | Nome: {bloco['nome_bloco']}")
    return True # Retorna True para indicar que há blocos

def cadastrar_sala_de_aula(id_sala, numero_sala, id_bloco, capacidade):
    """Cadastra uma nova SALA e a define como SALA_DE_AULA (em uma transação)."""
    conn = db_manager.get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    
    try:
        # 1. Insere na tabela 'Pai' (SALA)
        # O status padrão ao criar é 'Disponível'
        query_sala = """
        INSERT INTO SALA (id_sala, numero_sala, status, id_bloco) 
        VALUES (%s, %s, 'Disponível', %s)
        """
        cursor.execute(query_sala, (id_sala, numero_sala, id_bloco))
        
        # 2. Insere na tabela 'Filha' (SALA_DE_AULA)
        query_tipo = """
        INSERT INTO SALA_DE_AULA (id_sala, capacidade_alunos) 
        VALUES (%s, %s)
        """
        cursor.execute(query_tipo, (id_sala, capacidade))

        conn.commit()
        print(f"Sala de Aula '{numero_sala}' (ID: {id_sala}) cadastrada com sucesso.")

    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar Sala de Aula: {err}")
        if err.errno == 1062: # Duplicate entry
            print(f"Erro: O ID de sala '{id_sala}' já existe.")
        elif err.errno == 1452: # Foreign Key constraint fails
            print(f"Erro: O Bloco com ID '{id_bloco}' não existe.")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def cadastrar_laboratorio(id_sala, numero_sala, id_bloco, qtde_computadores):
    """Cadastra uma nova SALA e a define como LABORATORIO (em uma transação)."""
    conn = db_manager.get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    
    try:
        # 1. Insere na tabela 'Pai' (SALA)
        query_sala = """
        INSERT INTO SALA (id_sala, numero_sala, status, id_bloco) 
        VALUES (%s, %s, 'Disponível', %s)
        """
        cursor.execute(query_sala, (id_sala, numero_sala, id_bloco))
        
        # 2. Insere na tabela 'Filha' (LABORATORIO)
        query_tipo = """
        INSERT INTO LABORATORIO (id_sala, qtde_computadores) 
        VALUES (%s, %s)
        """
        cursor.execute(query_tipo, (id_sala, qtde_computadores))

        conn.commit()
        print(f"Laboratório '{numero_sala}' (ID: {id_sala}) cadastrado com sucesso.")

    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar Laboratório: {err}")
        if err.errno == 1062:
            print(f"Erro: O ID de sala '{id_sala}' já existe.")
        elif err.errno == 1452:
            print(f"Erro: O Bloco com ID '{id_bloco}' não existe.")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def cadastrar_escritorio(id_sala, numero_sala, id_bloco, setor_responsavel):
    """Cadastra uma nova SALA e a define como ESCRITORIO (em uma transação)."""
    conn = db_manager.get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    
    try:
        # 1. Insere na tabela 'Pai' (SALA)
        query_sala = """
        INSERT INTO SALA (id_sala, numero_sala, status, id_bloco) 
        VALUES (%s, %s, 'Disponível', %s)
        """
        cursor.execute(query_sala, (id_sala, numero_sala, id_bloco))
        
        # 2. Insere na tabela 'Filha' (ESCRITORIO)
        query_tipo = """
        INSERT INTO ESCRITORIO (id_sala, setor_responsavel) 
        VALUES (%s, %s)
        """
        cursor.execute(query_tipo, (id_sala, setor_responsavel))

        conn.commit()
        print(f"Escritório '{numero_sala}' (ID: {id_sala}) cadastrado com sucesso.")

    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar Escritório: {err}")
        if err.errno == 1062:
            print(f"Erro: O ID de sala '{id_sala}' já existe.")
        elif err.errno == 1452:
            print(f"Erro: O Bloco com ID '{id_bloco}' não existe.")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()