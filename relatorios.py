import db_manager

# -----------------------------------------------------------------
# 1. Professores por Departamento (Nome, Telefone)
# -----------------------------------------------------------------
def relatorio_professores_por_depto(departamento):
    print(f"\n--- Relatório: Professores do Depto. de '{departamento}' ---")
    
    query = """
    SELECT 
        p.nome, 
        p.telefone
    FROM PESSOA p
    JOIN PROFESSOR pr ON p.cpf = pr.cpf
    WHERE pr.departamento = %s
    """
    resultados = db_manager.execute_query(query, (departamento,))
    
    if not resultados:
        print(f"Nenhum professor encontrado para o departamento '{departamento}'.")
        return
    
    print(f"Encontrados {len(resultados)} professor(es):")
    print("Nome | Telefone")
    print("----------------------------------------")
    for r in resultados:
        print(f"{r['nome']} | {r['telefone']}")

# -----------------------------------------------------------------
# 2. Pessoa com a chave de uma sala específica (Nome)
# -----------------------------------------------------------------
def relatorio_pessoa_com_chave(numero_sala):
    print(f"\n--- Relatório: Pessoa atualmente com a chave da sala '{numero_sala}' ---")
    
    query = """
    SELECT 
        p.nome
    FROM SALA s
    JOIN CHAVE c ON s.id_sala = c.id_sala
    JOIN EMPRESTIMO e ON c.id_chave = e.id_chave
    JOIN PESSOA p ON e.cpf_pessoa = p.cpf
    WHERE 
        s.numero_sala = %s 
        AND e.data_hora_devolucao IS NULL
    """
    resultados = db_manager.execute_query(query, (numero_sala,)) 
    
    if not resultados:
        print(f"Ninguém está com a chave da sala '{numero_sala}' no momento, ou a sala não existe.")
    else:
        print(f"A pessoa com a chave é: {resultados[0]['nome']}")

# -----------------------------------------------------------------
# 3. Salas de Aula com capacidade > X (LISTA e COUNT)
# -----------------------------------------------------------------
def relatorio_contagem_salas_aula_maior_que(capacidade):
    print(f"\n--- Relatório: Salas de Aula com capacidade > {capacidade} ---")
    
    query = """
    SELECT 
        s.numero_sala,
        sa.capacidade_alunos
    FROM SALA_DE_AULA sa
    JOIN SALA s ON sa.id_sala = s.id_sala
    WHERE sa.capacidade_alunos > %s
    ORDER BY sa.capacidade_alunos DESC
    """
    resultados = db_manager.execute_query(query, (capacidade,))
    
    if not resultados:
        print(f"Nenhuma sala de aula encontrada com capacidade superior a {capacidade} alunos.")
    else:
        total_salas = len(resultados)
        print(f"Total de {total_salas} sala(s) encontrada(s) com capacidade superior a {capacidade} alunos:")
        print("----------------------------------------")
        print("Sala | Capacidade")
        print("----------------------------------------")
        for r in resultados:
            print(f"{r['numero_sala']} | {r['capacidade_alunos']} alunos")
# -----------------------------------------------------------------
# 4. Salas por Status (Numero)
# -----------------------------------------------------------------
def relatorio_salas_por_status(status):
    print(f"\n--- Relatório: Salas com status '{status}' ---")
    
    query = """
    SELECT numero_sala
    FROM SALA
    WHERE status = %s
    """
    resultados = db_manager.execute_query(query, (status,))
    
    if not resultados:
        print(f"Nenhuma sala encontrada com o status '{status}'.")
        return
    
    print(f"Salas com status '{status}':")
    for r in resultados:
        print(f"- Sala: {r['numero_sala']}")

# -----------------------------------------------------------------
# 5. Servidores Técnicos (Nome, Setor) ordenado por Nome
# (Este relatório não precisava de parâmetros)
# -----------------------------------------------------------------
def relatorio_servidores_tecnicos_setor():
    print("\n--- Relatório: Servidores Técnicos e seus Setores (Ordenado por Nome) ---")
    
    query = """
    SELECT 
        p.nome, 
        st.setor
    FROM PESSOA p
    JOIN SERVIDOR_TECNICO st ON p.cpf = st.cpf
    ORDER BY p.nome ASC
    """
    resultados = db_manager.execute_query(query)
    
    if not resultados:
        print("Nenhum servidor técnico cadastrado.")
        return
    
    print("Nome | Setor")
    print("----------------------------------------")
    for r in resultados:
        print(f"{r['nome']} | {r['setor']}")

# -----------------------------------------------------------------
# 6. Funcionário com mais retiradas (Nome)
# (Este relatório não precisava de parâmetros)
# -----------------------------------------------------------------
def relatorio_funcionario_mais_retiradas():
    print("\n--- Relatório: Funcionário com Mais Registros de Retirada ---")
    
    query = """
    SELECT 
        f.nome_funcionario, 
        COUNT(e.id_emprestimo) as total_retiradas
    FROM FUNCIONARIO f
    JOIN EMPRESTIMO e ON f.id_funcionario = e.id_funcionario_retirada
    GROUP BY f.id_funcionario, f.nome_funcionario
    ORDER BY total_retiradas DESC
    LIMIT 1
    """
    resultados = db_manager.execute_query(query)
    
    if not resultados:
        print("Nenhum registro de empréstimo encontrado.")
    else:
        r = resultados[0]
        print(f"Funcionário com mais retiradas: {r['nome_funcionario']} (Total: {r['total_retiradas']} retiradas)")

# Em relatorios.py
# (Certifique-se de que 'import db_manager' está no topo do arquivo)

# -----------------------------------------------------------------
# 7. Chaves por Bloco (Codigo Visual)
# -----------------------------------------------------------------
def relatorio_chaves_por_bloco():
    print("\n--- Relatório: Chaves por Bloco ---")
    
    # 1. Listar todos os blocos disponíveis
    print("Buscando blocos cadastrados...")
    query_blocos = "SELECT id_bloco, nome_bloco FROM BLOCO ORDER BY nome_bloco"
    blocos = db_manager.execute_query(query_blocos)
    
    if not blocos:
        print("Erro: Nenhum bloco foi cadastrado no sistema.")
        print("É necessário cadastrar um bloco antes de consultar suas chaves.")
        return
        
    print("\n--- Blocos Disponíveis ---")
    for b in blocos:
        print(f"ID: {b['id_bloco']} | Nome: {b['nome_bloco']}")
    
    # 2. Pedir o ID ao usuário
    try:
        id_bloco_desejado = int(input("\nDigite o ID do Bloco que deseja consultar: "))
    except ValueError:
        print("Erro: ID inválido. Deve ser um número.")
        return

    # 3. Buscar as chaves para o ID selecionado
    query_chaves = """
    SELECT 
        c.codigo_visual,
        s.numero_sala
    FROM BLOCO b
    JOIN SALA s ON b.id_bloco = s.id_bloco
    JOIN CHAVE c ON s.id_sala = c.id_sala
    WHERE b.id_bloco = %s
    """
    resultados = db_manager.execute_query(query_chaves, (id_bloco_desejado,))
    
    # 4. Exibir os resultados
    if not resultados:
        # Verifica se o bloco ao menos existia
        bloco_encontrado = next((item for item in blocos if item["id_bloco"] == id_bloco_desejado), None)
        if not bloco_encontrado:
             print(f"Erro: O Bloco com ID {id_bloco_desejado} não existe.")
        else:
             print(f"Nenhuma chave encontrada para o bloco com ID {id_bloco_desejado} ({bloco_encontrado['nome_bloco']}).")
        return
    
    # Pega o nome do bloco para exibir no título
    nome_bloco_selecionado = next(item['nome_bloco'] for item in blocos if item["id_bloco"] == id_bloco_desejado)
    
    print(f"\n--- Chaves encontradas no '{nome_bloco_selecionado}' (ID: {id_bloco_desejado}) ---")
    print("Código Visual | Sala")
    print("-------------------------")
    for r in resultados:
        print(f"- {r['codigo_visual']} (Sala: {r['numero_sala']})")

# -----------------------------------------------------------------
# 8. Sala com mais computadores (Numero, Status)
# (Este relatório não precisava de parâmetros)
# -----------------------------------------------------------------
def relatorio_laboratorio_mais_computadores():
    print("\n--- Relatório: Laboratório com Maior Quantidade de Computadores ---")
    
    query = """
    SELECT 
        s.numero_sala, 
        s.status,
        l.qtde_computadores
    FROM SALA s
    JOIN LABORATORIO l ON s.id_sala = l.id_sala
    ORDER BY l.qtde_computadores DESC
    LIMIT 1
    """
    resultados = db_manager.execute_query(query)
    
    if not resultados:
        print("Nenhum laboratório cadastrado.")
    else:
        r = resultados[0]
        print(f"Sala: {r['numero_sala']} (com {r['qtde_computadores']} computadores)")
        print(f"Status Atual: {r['status']}")

# -----------------------------------------------------------------
# 9. Empréstimos em data específica (ID, Nome Pessoa, Nome Funcionário)
# -----------------------------------------------------------------
def relatorio_emprestimos_por_data(data_consulta):
    print(f"\n--- Relatório: Empréstimos realizados em {data_consulta} ---")
    
    query = """
    SELECT 
        e.id_emprestimo,
        p.nome as nome_pessoa,
        f.nome_funcionario as nome_funcionario
    FROM EMPRESTIMO e
    JOIN PESSOA p ON e.cpf_pessoa = p.cpf
    JOIN FUNCIONARIO f ON e.id_funcionario_retirada = f.id_funcionario
    WHERE DATE(e.data_hora_retirada) = %s
    """
    # Validação simples da data (formato YYYY-MM-DD)
    try:
        if len(data_consulta) != 10 or data_consulta[4] != '-' or data_consulta[7] != '-':
            raise ValueError("Formato de data inválido. Use YYYY-MM-DD.")
        
        resultados = db_manager.execute_query(query, (data_consulta,))
        
        if not resultados:
            print(f"Nenhum empréstimo encontrado para a data {data_consulta}.")
            return
        
        print("ID Empréstimo | Nome da Pessoa | Nome do Funcionário (Retirada)")
        print("------------------------------------------------------------------")
        for r in resultados:
            print(f"{r['id_emprestimo']} | {r['nome_pessoa']} | {r['nome_funcionario']}")
            
    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro ao consultar o banco: {e}")


# -----------------------------------------------------------------
# 10. Chaves (com empréstimo) cuja sala NÃO está 'Indisponível'
# (Este relatório não precisava de parâmetros)
# -----------------------------------------------------------------
def relatorio_discrepancia_status_sala():
    print("\n--- Relatório: (Discrepância) Chaves com Empréstimo Ativo mas Sala NÃO 'Indisponível' ---")
    
    query = """
    SELECT DISTINCT
        c.codigo_visual,
        s.numero_sala,
        s.status as status_atual
    FROM CHAVE c
    JOIN SALA s ON c.id_sala = s.id_sala
    JOIN EMPRESTIMO e ON c.id_chave = e.id_chave
    WHERE 
        e.data_hora_devolucao IS NULL 
        AND s.status != 'Indisponível'
    """
    resultados = db_manager.execute_query(query)
    
    if not resultados:
        print("Nenhuma discrepância encontrada. Todos os empréstimos ativos parecem ter salas 'Indisponível'.")
        return
    
    print("Discrepâncias encontradas (Empréstimo Ativo / Status de Sala Incorreto):")
    print("Código Chave | Sala | Status Atual (Incorreto)")
    print("-----------------------------------------------")
    for r in resultados:
        print(f"{r['codigo_visual']} | {r['numero_sala']} | {r['status_atual']}")