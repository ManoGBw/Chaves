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

def main_menu():
    """Exibe o menu principal e gerencia a navegação."""
    while True:
        print("\n======================================")
        print("   Sistema de Controle de Chaves   ")
        print("======================================")
        print("1. Realizar Empréstimo de Chave")
        print("2. Realizar Devolução de Chave")
        print("3. Consultar Chaves Disponíveis")
        print("4. (TODO) Cadastrar Nova Pessoa")
        print("5. (TODO) Cadastrar Nova Sala")
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
            print("Função de cadastro ainda não implementada.")
        elif opcao == '5':
            print("Função de cadastro ainda não implementada.")
        elif opcao == '0':
            print("Saindo do sistema...")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()