# relatorios.py
# Este arquivo contém funções para gerar relatórios de consulta ao banco de dados.

import db_manager

# -----------------------------------------------------------------
# 1. Professores de Informática (Nome, Telefone)
# -----------------------------------------------------------------
def relatorio_professores_informatica():
    print("\n--- Relatório: Professores do Depto. de Informática ---")
    
    query = """
    SELECT 
        p.nome, 
        p.telefone
    FROM PESSOA p
    JOIN PROFESSOR pr ON p.cpf = pr.cpf
    WHERE pr.departamento = 'Informática'
    """
    resultados = db_manager.execute_query(query)
    
    if not resultados:
        print("Nenhum professor encontrado para o departamento 'Informática'.")
        return
    
    print(f"Encontrados {len(resultados)} professor(es):")
    print("Nome | Telefone")
    print("----------------------------------------")
    for r in resultados:
        print(f"{r['nome']} | {r['telefone']}")

# -----------------------------------------------------------------
# 2. Pessoa com a chave '102' (Nome)
# -----------------------------------------------------------------
def relatorio_pessoa_com_chave_102():
    print("\n--- Relatório: Pessoa atualmente com a chave da sala '102' ---")
    
    query = """
    SELECT 
        p.nome
    FROM SALA s
    JOIN CHAVE c ON s.id_sala = c.id_sala
    JOIN EMPRESTIMO e ON c.id_chave = e.id_chave
    JOIN PESSOA p ON e.cpf_pessoa = p.cpf
    WHERE 
        s.numero_sala = '102' 
        AND e.data_hora_devolucao IS NULL
    """
    resultados = db_manager.execute_query(query) 
    
    if not resultados:
        print("Ninguém está com a chave da sala '102' no momento, ou a sala não existe.")
    else:
        
        print(f"A pessoa com a chave é: {resultados[0]['nome']}")

# -----------------------------------------------------------------
# 3. Salas de Aula com capacidade > 45 (COUNT)
# -----------------------------------------------------------------
def relatorio_contagem_salas_aula_maior_45():
    print("\n--- Relatório: Quantidade de Salas de Aula com capacidade > 45 ---")
    
    query = """
    SELECT COUNT(id_sala) as total
    FROM SALA_DE_AULA
    WHERE capacidade_alunos > 45
    """
    resultados = db_manager.execute_query(query)
    
    if not resultados:
        print("Erro ao executar a contagem.")
    else:
        print(f"Total de salas com capacidade superior a 45 alunos: {resultados[0]['total']}")

# -----------------------------------------------------------------
# 4. Salas 'Em Manutenção' (Numero)
# -----------------------------------------------------------------
def relatorio_salas_em_manutencao():
    print("\n--- Relatório: Salas em 'Em Manutenção' ---")
    
    query = """
    SELECT numero_sala
    FROM SALA
    WHERE status = 'Em Manutenção'
    """
    resultados = db_manager.execute_query(query)
    
    if not resultados:
        print("Nenhuma sala encontrada com o status 'Em Manutenção'.")
        return
    
    print("Salas em Manutenção:")
    for r in resultados:
        print(f"- Sala: {r['numero_sala']}")

# -----------------------------------------------------------------
# 5. Servidores Técnicos (Nome, Setor) ordenado por Nome
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

# -----------------------------------------------------------------
# 7. Chaves do 'Bloco B - Laboratórios' (Codigo Visual)
# -----------------------------------------------------------------
def relatorio_chaves_bloco_b_labs():
    print("\n--- Relatório: Chaves do 'Bloco B - Laboratórios' ---")
    nome_bloco = 'Bloco B - Laboratórios'
    
    query = """
    SELECT 
        c.codigo_visual
    FROM BLOCO b
    JOIN SALA s ON b.id_bloco = s.id_bloco
    JOIN CHAVE c ON s.id_sala = c.id_sala
    WHERE b.nome_bloco = %s
    """
    resultados = db_manager.execute_query(query, (nome_bloco,))
    
    if not resultados:
        print(f"Nenhuma chave encontrada para o bloco '{nome_bloco}'.")
        return
    
    print(f"Códigos Visuais das Chaves no '{nome_bloco}':")
    for r in resultados:
        print(f"- {r['codigo_visual']}")

# -----------------------------------------------------------------
# 8. Sala com mais computadores (Numero, Status)
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
# 9. Empréstimos em '2025-10-15' (ID, Nome Pessoa, Nome Funcionário)
# -----------------------------------------------------------------
def relatorio_emprestimos_data_especifica():
    data_consulta = '2025-10-15'
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
    resultados = db_manager.execute_query(query, (data_consulta,))
    
    if not resultados:
        print(f"Nenhum empréstimo encontrado para a data {data_consulta}.")
        return
    
    print("ID Empréstimo | Nome da Pessoa | Nome do Funcionário (Retirada)")
    print("------------------------------------------------------------------")
    for r in resultados:
        print(f"{r['id_emprestimo']} | {r['nome_pessoa']} | {r['nome_funcionario']}")

# -----------------------------------------------------------------
# 10. Chaves (com empréstimo) cuja sala NÃO está 'Indisponível'
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