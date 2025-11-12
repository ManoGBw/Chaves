import operacoes_db
import relatorios 
import sys

def menu_emprestimo():
    print("\n== Registrar Empréstimo ==")
    cpf = input("CPF da Pessoa (só números, ex: 12345678900): ")
    codigo_chave = input("Código Visual da Chave: ")
    id_funcionario = input("ID do Funcionário da portaria: ") 
    
    if not (cpf and codigo_chave and id_funcionario):
        print("Erro: Todos os campos são obrigatórios.")
        return
    
    try:
        operacoes_db.realizar_emprestimo(cpf, codigo_chave, int(id_funcionario))
    except ValueError:
        print("Erro: ID do Funcionário deve ser um número.")


def menu_devolucao():
    print("\n== Registrar Devolução ==")
    codigo_chave = input("Código Visual da Chave: ")
    id_funcionario = input("ID do Funcionário da portaria: ")

    if not (codigo_chave and id_funcionario):
        print("Erro: Todos os campos são obrigatórios.")
        return
        
    try:
        operacoes_db.realizar_devolucao(codigo_chave, int(id_funcionario))
    except ValueError:
        print("Erro: ID do Funcionário deve ser um número.")

def menu_cadastrar_aluno():
    print("\n== Cadastrar Novo Aluno ==")
    cpf = input("CPF (ex: 12345678900): ")
    nome = input("Nome Completo: ")
    telefone = input("Telefone (ex: 55912345678): ")
    matricula = input("Número de Matrícula: ")
    
    if not (cpf and nome and matricula):
        print("Erro: CPF, Nome e Matrícula são obrigatórios.")
        return
    
    operacoes_db.cadastrar_aluno(cpf, nome, telefone, matricula)

def menu_cadastrar_professor():
    print("\n== Cadastrar Novo Professor ==")
    cpf = input("CPF (ex: 12345678900): ")
    nome = input("Nome Completo: ")
    telefone = input("Telefone (ex: 55912345678): ")
    siape = input("SIAPE: ")
    departamento = input("Departamento: ")

    if not (cpf and nome and siape):
        print("Erro: CPF, Nome e SIAPE são obrigatórios.")
        return

    operacoes_db.cadastrar_professor(cpf, nome, telefone, siape, departamento)

def menu_cadastrar_servidor():
    print("\n== Cadastrar Novo Servidor Técnico ==")
    cpf = input("CPF (ex: 12345678900): ")
    nome = input("Nome Completo: ")
    telefone = input("Telefone (ex: 55912345678): ")
    siape = input("SIAPE: ")
    setor = input("Setor: ")

    if not (cpf and nome and siape):
        print("Erro: CPF, Nome e SIAPE são obrigatórios.")
        return

    operacoes_db.cadastrar_servidor_tecnico(cpf, nome, telefone, siape, setor)


def menu_cadastro_pessoa():
    while True:
        print("\n--- Cadastrar Nova Pessoa ---")
        print("1. Cadastrar Aluno")
        print("2. Cadastrar Professor")
        print("3. Cadastrar Servidor Técnico")
        print("0. Voltar ao Menu Principal")
        
        opcao_pessoa = input("Escolha o tipo de pessoa: ")
        
        if opcao_pessoa == '1':
            menu_cadastrar_aluno()
        elif opcao_pessoa == '2':
            menu_cadastrar_professor()
        elif opcao_pessoa == '3':
            menu_cadastrar_servidor()
        elif opcao_pessoa == '0':
            break
        else:
            print("Opção inválida.")

def menu_cadastro_sala():
    """Exibe o sub-menu para cadastro de tipos de sala."""
    while True:
        print("\n--- Cadastrar Nova Sala ---")
        print("1. Cadastrar Sala de Aula")
        print("2. Cadastrar Laboratório")
        print("3. Cadastrar Escritório")
        print("0. Voltar ao Menu Principal")
        
        opcao_sala = input("Escolha o tipo de sala: ")
        
        if opcao_sala == '0':
            break

        print("Buscando blocos...")
        if not operacoes_db.listar_blocos():
            continue 
            
        print("\n--- Preencha os dados da Sala ---")
        try:
            numero_sala = input("Número/Nome da Sala (ex: '101A' ou 'Lab de Redes'): ")
            id_bloco = int(input("ID do Bloco (veja lista acima): "))
            codigo_visual = input("Código Visual da Chave para esta sala (ex: CHV-A101): ")

            if not numero_sala or not codigo_visual:
                print("Erro: O Nome/Número da sala e o Código Visual são obrigatórios.")
                continue

        except ValueError:
            print("Erro: ID do Bloco deve ser um número.")
            continue

        if opcao_sala == '1':
            try:
                capacidade = int(input("Capacidade de Alunos: "))
                operacoes_db.cadastrar_sala_de_aula(numero_sala, id_bloco, capacidade, codigo_visual)
            except ValueError:
                print("Erro: Capacidade deve ser um número.")
                
        elif opcao_sala == '2':
            try:
                qtde = int(input("Quantidade de Computadores: "))
                operacoes_db.cadastrar_laboratorio(numero_sala, id_bloco, qtde, codigo_visual)
            except ValueError:
                print("Erro: Quantidade deve ser um número.")
                
        elif opcao_sala == '3':
            setor = input("Setor Responsável: ")
            if not setor:
                print("Erro: Setor é obrigatório.")
                continue
            operacoes_db.cadastrar_escritorio(numero_sala, id_bloco, setor, codigo_visual)
            
        else:
            print("Opção inválida.")

# --- MENU DE RELATÓRIOS ATUALIZADO ---
def menu_relatorios():
    """Exibe o sub-menu para geração de relatórios."""
    while True:
        print("\n--- Menu de Relatórios ---")
        print("1. Professores por Departamento")
        print("2. Quem está com a chave de uma sala")
        print("3. Contagem de salas de aula (Capacidade > X)")
        print("4. Salas por Status (Ex: Em Manutenção)")
        print("5. Servidores Técnicos e Setores (Ordenado)")
        print("6. Funcionário com mais retiradas")
        print("7. Chaves por Bloco")
        print("8. Laboratório com mais computadores")
        print("9. Empréstimos em data específica")
        print("10. Discrepância: Empréstimo ativo mas sala não 'Indisponível'")
        print("0. Voltar ao Menu Principal")
        
        opcao_rel = input("Escolha um relatório: ")

        if opcao_rel == '1':
            depto = input("Digite o nome do Departamento (ex: Informática, Engenharia ou TI): ")
            if depto:
                relatorios.relatorio_professores_por_depto(depto)
            else:
                print("Erro: Departamento não pode ser vazio.")
                
        elif opcao_rel == '2':
            sala = input("Digite o Número da Sala (ex: 102): ")
            if sala:
                relatorios.relatorio_pessoa_com_chave(sala)
            else:
                print("Erro: Número da sala não pode ser vazio.")

        elif opcao_rel == '3':
            try:
                capacidade = int(input("Digite a capacidade mínima (ex: 45): "))
                relatorios.relatorio_contagem_salas_aula_maior_que(capacidade)
            except ValueError:
                print("Erro: Capacidade deve ser um número.")
                
        elif opcao_rel == '4':
            status = input("Digite o Status da Sala (ex: Em Manutenção, Disponível, Indisponível): ")
            if status:
                relatorios.relatorio_salas_por_status(status)
            else:
                print("Erro: Status não pode ser vazio.")

        elif opcao_rel == '5':
            relatorios.relatorio_servidores_tecnicos_setor()

        elif opcao_rel == '6':
            relatorios.relatorio_funcionario_mais_retiradas()

        elif opcao_rel == '7':
            bloco = input("Digite o Nome do Bloco (ex: Bloco B - Laboratórios): ")
            if bloco:
                relatorios.relatorio_chaves_por_bloco(bloco)
            else:
                print("Erro: Nome do bloco não pode ser vazio.")

        elif opcao_rel == '8':
            relatorios.relatorio_laboratorio_mais_computadores()

        elif opcao_rel == '9':
            data = input("Digite a data da consulta (Formato YYYY-MM-DD): ")
            if data:
                relatorios.relatorio_emprestimos_por_data(data)
            else:
                print("Erro: Data não pode ser vazia.")

        elif opcao_rel == '10':
            relatorios.relatorio_discrepancia_status_sala()

        elif opcao_rel == '0':
            break
        else:
            print("Opção inválida.")

# --- MENU PRINCIPAL (Sem mudanças, mas incluído para completude) ---
def main_menu():
    while True:
        print("\n======================================")
        print("   Sistema de Controle de Chaves   ")
        print("======================================")
        print("1. Realizar Empréstimo de Chave")
        print("2. Realizar Devolução de Chave")
        print("3. Consultar Chaves Disponíveis")
        print("4. Cadastrar Nova Pessoa")
        print("5. Cadastrar Nova Sala")
        print("6. Acessar Relatórios") 
        print("0. Sair")
        print("--------------------------------------")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_emprestimo()
        elif opcao == '2':
            menu_devolucao()
        elif opcao == '3':
            operacoes_db.verificar_chaves_disponis()
        elif opcao == '4':
            menu_cadastro_pessoa()
        elif opcao == '5':
            menu_cadastro_sala()
        elif opcao == '6':        
            menu_relatorios()
        elif opcao == '0':
            print("Saindo do sistema...")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()