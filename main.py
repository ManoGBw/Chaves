# main.py
import operacoes_db
import sys

def menu_emprestimo():
    """Coleta dados para realizar um empréstimo."""
    print("\n== Registrar Empréstimo ==")
    cpf = input("CPF da Pessoa (só números, ex: 12345678900): ")
    codigo_chave = input("Código Visual da Chave: ")
    # <-- MUDANÇA: Pedimos o ID numérico do funcionário
    id_funcionario = input("ID do Funcionário da portaria: ") 
    
    if not (cpf and codigo_chave and id_funcionario):
        print("Erro: Todos os campos são obrigatórios.")
        return
    
    # <-- MUDANÇA: Passamos o id_funcionario
    operacoes_db.realizar_emprestimo(cpf, codigo_chave, int(id_funcionario))

def menu_devolucao():
    """Coleta dados para realizar uma devolução."""
    print("\n== Registrar Devolução ==")
    codigo_chave = input("Código Visual da Chave: ")
    # <-- MUDANÇA: Pedimos o ID numérico do funcionário
    id_funcionario = input("ID do Funcionário da portaria: ")

    if not (codigo_chave and id_funcionario):
        print("Erro: Todos os campos são obrigatórios.")
        return
        
    # <-- MUDANÇA: Passamos o id_funcionario
    operacoes_db.realizar_devolucao(codigo_chave, int(id_funcionario))

def menu_cadastrar_aluno():
    """Coleta dados para cadastrar um novo aluno."""
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
    """Coleta dados para cadastrar um novo professor."""
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
    """Coleta dados para cadastrar um novo servidor técnico."""
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
    """Exibe o sub-menu para cadastro de tipos de pessoa."""
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
            break # Volta ao menu principal
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
            break # Volta ao menu principal

        # Antes de pedir dados, lista os blocos existentes
        print("Buscando blocos...")
        if not operacoes_db.listar_blocos():
            # Se não houver blocos, não podemos cadastrar salas
            continue # Volta ao menu de cadastro de sala
            
        print("\n--- Preencha os dados da Sala ---")
        try:
            # Coleta informações comuns a todas as salas
            id_sala = int(input("ID da Sala (número ex: 101): "))
            numero_sala = input("Número/Nome da Sala (ex: '101A' ou 'Lab de Redes'): ")
            id_bloco = int(input("ID do Bloco (veja lista acima): "))
        except ValueError:
            print("Erro: ID da Sala e ID do Bloco devem ser números.")
            continue

        # Coleta informações específicas do tipo de sala
        if opcao_sala == '1':
            try:
                capacidade = int(input("Capacidade de Alunos: "))
                operacoes_db.cadastrar_sala_de_aula(id_sala, numero_sala, id_bloco, capacidade)
            except ValueError:
                print("Erro: Capacidade deve ser um número.")
                
        elif opcao_sala == '2':
            try:
                qtde = int(input("Quantidade de Computadores: "))
                operacoes_db.cadastrar_laboratorio(id_sala, numero_sala, id_bloco, qtde)
            except ValueError:
                print("Erro: Quantidade deve ser um número.")
                
        elif opcao_sala == '3':
            setor = input("Setor Responsável: ")
            if not setor:
                print("Erro: Setor é obrigatório.")
                continue
            operacoes_db.cadastrar_escritorio(id_sala, numero_sala, id_bloco, setor)
            
        else:
            print("Opção inválida.")


def main_menu():
    """Exibe o menu principal e gerencia a navegação."""
    while True:
        print("\n======================================")
        print("   Sistema de Controle de Chaves   ")
        print("======================================")
        print("1. Realizar Empréstimo de Chave")
        print("2. Realizar Devolução de Chave")
        print("3. Consultar Chaves Disponíveis")
        print("4. Cadastrar Nova Pessoa")
        print("5. Cadastrar Nova Sala") # <-- MUDANÇA AQUI
        print("0. Sair")
        print("--------------------------------------")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_emprestimo()
        elif opcao == '2':
            menu_devolucao()
        elif opcao == '3':
            operacoes_db.verificar_chaves_disponiveis()
        elif opcao == '4':
            menu_cadastro_pessoa()
        elif opcao == '5':
            menu_cadastro_sala() # <-- MUDANÇA AQUI
        elif opcao == '0':
            print("Saindo do sistema...")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()