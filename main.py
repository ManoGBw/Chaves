import operacoes_db
import sys

def menu_emprestimo():
    print("\n== Registrar Empréstimo ==")
    cpf = input("CPF da Pessoa (só números, ex: 12345678900): ")
    codigo_chave = input("Código Visual da Chave: ")
    id_funcionario = input("ID do Funcionário da portaria: ") 
    
    if not (cpf and codigo_chave and id_funcionario):
        print("Erro: Todos os campos são obrigatórios.")
        return
    
    operacoes_db.realizar_emprestimo(cpf, codigo_chave, int(id_funcionario))

def menu_devolucao():
    print("\n== Registrar Devolução ==")
    codigo_chave = input("Código Visual da Chave: ")
    id_funcionario = input("ID do Funcionário da portaria: ")

    if not (codigo_chave and id_funcionario):
        print("Erro: Todos os campos são obrigatórios.")
        return
        
    operacoes_db.realizar_devolucao(codigo_chave, int(id_funcionario))

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

# main.py

# ... (funções anteriores ficam iguais) ...

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
            # --- MUDANÇA AQUI ---
            operacoes_db.cadastrar_escritorio(numero_sala, id_bloco, setor, codigo_visual)
            
        else:
            print("Opção inválida.")

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
            menu_cadastro_sala()
        elif opcao == '0':
            print("Saindo do sistema...")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()