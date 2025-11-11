# operacoes_db.py
import db_manager
from datetime import datetime
import mysql.connector # Importar para tratar erros específicos

def verificar_chaves_disponiveis():
    """Consulta e exibe todas as chaves com status 'Disponível'."""
    print("\n--- Chaves Disponíveis ---")
    
    # <-- MUDANÇA: Query ajustada para suas tabelas e colunas
    # Juntamos Bloco, Sala e Chave para dar uma informação completa
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