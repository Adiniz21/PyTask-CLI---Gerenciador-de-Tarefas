import os
import usuario
import tarefa
import endereco

def limpa_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu_principal():
    print("Você acaba de iniciar o sistema para armazenar as tarefas")

    while True:
        print("Escolha uma das opções abaixo:")
        print("1 - Deseja fazer um cadastro de um novo usuário")
        print("2 - Deseja fazer o Login")
        print("3 - Deseja Sair do sistema")
        
        try:
            escolha = int(input("Escolha uma opção: "))
        except ValueError:
            print("Escolha um opção válida")
            input("Pressione ENTER para continuar...")
            continue
        
        match escolha:
            case 1:
                limpa_tela()
                usuario.cadastro_usuario()  
            case 2:
                limpa_tela()
                usuario.Login()
            case 3:
                limpa_tela()
                print("Você escolheu sair do sistema.")
                break         
            case _:
                limpa_tela()
                print("Escolha uma opção válida")
                input("Pressione ENTER para continuar...")
                continue

def menu_usuario_logado(id, email):
    while True:
        limpa_tela()
        print("Escolha uma das opções abaixo:")
        print("1 - Deseja alterar uma informação do usuário")
        print("2 - Deseja Excluir o usuário")
        print("3 - Deseja alterar uma informação do endereço")
        print("4 - Deseja adicionar uma tarefa")
        print("5 - Deseja listar as tarefas")
        print("6 - Deseja alterar uma tarefa")
        print("7 - Excluir uma tarefa")
        print("8 - Deslogar do sistema")

        try:
            escolha = int(input("Escolha uma opção: "))
        except ValueError:
            print("Escolha um opção válida")
            input("Pressione ENTER para continuar...")
            continue

        match escolha:
            case 1:
                limpa_tela()
                print("\n[LOG] Iniciando alteração de dados do usuário...")
                usuario.altera_usuario(id)                

            case 2:
                limpa_tela()
                print("\n[LOG] Iniciando exclusão de dados do usuário...")
                resultado = usuario.excluir(id)
                if resultado == "sim":
                    break                
                
            case 3:
                limpa_tela()
                print("\n[LOG] Iniciando alteração de endereço via API...")
                endereco.altera_endereco(id)
                
            case 4:
                limpa_tela()
                print("\n[LOG] Preparando formulário de nova tarefa...")
                tarefa.cria_tarefa(id)
                
                
            case 5:
                print("\n[LOG] Buscando tarefas no banco de dados...")
                tarefa.lista_tarefas(id)
                
            case 6:
                print("\n[LOG] Editando tarefa existente...")
                tarefa.altera_tarefa(id)

            case 7:
                print("\n[LOG] Excluindo tarefa existente...")
                tarefa.deleta_tarefa(id)
                
            case 8:
                limpa_tela()
                print(f"Até logo, {email}! Saindo...")
                input("Pressione ENTER para continuar...")
                limpa_tela()
                break # Encerra o loop e desloga
                
            case _:
                print("Opção inválida! Tente um número de 1 a 8.")


