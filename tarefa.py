import config
import database 

import datetime

def cria_tarefa(id):
    campos = ["Título", "Descrição", "Prioridade", "Status", "Categoria", "Prazo"]
    dados_tarefa = {}

    for campo in campos:
        while True:
            valor = input(f"{campo} da Tarefa: ").strip()
            
            # Validação específica para o campo Prazo
            if campo == "Prazo":
                try:
                    # Tenta converter o que o usuário digitou para o formato de data
                    # Exemplo: 31/12/2026
                    data_formatada = datetime.datetime.strptime(valor, "%d/%m/%Y").date()
                    dados_tarefa[campo.lower()] = data_formatada
                    break
                except ValueError:
                    print("Erro: Formato de data inválido! Use DD/MM/AAAA (ex: 31/03/2026)")
                    continue

            if valor:
                dados_tarefa[campo.lower()] = valor
                break
            print(f"Erro: O campo {campo} não pode ficar vazio!")

    # Bloco de inserção no banco (não precisa de While True se os dados já estão validados)
    conexao = None
    try:
        conexao = database.conectar()
        cursor = conexao.cursor(dictionary=True)

        sql_endereco = "SELECT id FROM endereco WHERE usuario_id = %s"
        cursor.execute(sql_endereco, (id,))
        resultado_endereco = cursor.fetchone()

        if not resultado_endereco:
            print("Erro: Usuário sem endereço cadastrado.")
            return # Sai da função

        id_final_endereco = resultado_endereco['id']

        sql_tarefa = """
            INSERT INTO tarefas 
            (usuario_id, endereco_id, titulo, descricao, prioridade, status, categoria, data_criacao, prazo) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s)
        """
        
        values_tarefa = (
            id, 
            id_final_endereco, 
            dados_tarefa["título"], 
            dados_tarefa["descrição"], 
            dados_tarefa["prioridade"], 
            dados_tarefa["status"], 
            dados_tarefa["categoria"], 
            dados_tarefa["prazo"]
        )

        cursor.execute(sql_tarefa, values_tarefa)
        conexao.commit()
        print("Tarefa adicionada com sucesso!")
        input("Pressione ENTER para continuar . . .")

    except Exception as e:
        print(f"Erro ao adicionar tarefa no banco: {e}")
    finally:
        if conexao:
            cursor.close()
            conexao.close()
        


def lista_tarefas(id):
    try:
        conexao = database.conectar()
        cursor = conexao.cursor(dictionary=True)
        sql = "select * from tarefas where usuario_id = %s"
        values = (id, )
        cursor.execute(sql, values)

        dados = cursor.fetchall()
        # Largura total ajustada para ~105 caracteres (cabe na maioria dos terminais)
        largura_total = 105
        linha_separadora = "-" * largura_total

        # Cabeçalho com nomes encurtados e tamanhos menores
        print("\n" + linha_separadora)
        print(f"| {'ID':<3} | {'TÍTULO':<18} | {'DESCRIÇÃO':<25} | {'PRIOR':<8} | {'STATUS':<10} | {'CAT':<12} | {'PRAZO':<10} |")
        print(linha_separadora)

        if dados:
            for dado in dados:
                # 1. Pegando os valores
                id_t = str(dado.get('id', ''))[:3]
                tit  = str(dado.get('titulo', ''))[:18]    # Corta em 18
                desc = str(dado.get('descricao', ''))[:25] # Corta em 25
                prio = str(dado.get('prioridade', ''))[:8]
                st   = str(dado.get('status', ''))[:10]
                cat  = str(dado.get('categoria', ''))[:12]
                
                # 2. Formatando o Prazo (Apenas DD/MM/AAAA)
                prazo_raw = dado.get('prazo')
                if prazo_raw:
                    # Tenta formatar se for objeto datetime, senão apenas fatia a string
                    try:
                        praz = prazo_raw.strftime('%d/%m/%y') # Formato 17/03/26
                    except:
                        praz = str(prazo_raw)[:10]
                else:
                    praz = "---"

                # 3. Exibindo a linha (Note que os números batem com o cabeçalho)
                print(f"| {id_t:<3} | {tit:<18} | {desc:<25} | {prio:<8} | {st:<10} | {cat:<12} | {praz:<10} |")
        else:
            print(f"| {' ':<3} | {'Nenhuma tarefa encontrada':<95} |")

        print(linha_separadora)

        cursor.close()
        conexao.close()

        input("\n Pressione ENTER para prosseguir . . .")
    except:
        print("Não foi possível listar as tarefas")

import datetime

def altera_tarefa(id_usuario_logado):
    while True:
        try:
            print("\n" + "="*30)
            id_input = input("Informe o ID da tarefa para alterar (ou 'S' para sair): ").strip()
            
            if id_input.upper() == 'S':
                break
            
            id_tarefa = int(id_input)
        except ValueError:
            print("Erro: O ID deve ser um número inteiro.")
            continue

        conexao = None
        cursor = None
        try:
            conexao = database.conectar()
            cursor = conexao.cursor(dictionary=True)

            # 1. Validação de Segurança: A tarefa existe E pertence ao usuário logado?
            sql_check = "SELECT titulo FROM tarefas WHERE id = %s AND usuario_id = %s"
            cursor.execute(sql_check, (id_tarefa, id_usuario_logado))
            tarefa = cursor.fetchone()

            if not tarefa:
                print(f"Aviso: Tarefa ID {id_tarefa} não encontrada ou você não tem permissão para alterá-la.")
                continue

            # 2. Menu de Alteração
            print(f"\nTarefa encontrada: {tarefa['titulo']}")
            print("1 - Alterar Título")
            print("2 - Alterar Descrição")
            print("3 - Alterar Prioridade")
            print("4 - Alterar Status")
            print("5 - Alterar Categoria")
            print("6 - Alterar Prazo")
            print("0 - Cancelar")

            opcao = input("\nO que você deseja alterar? ")

            if opcao == '0':
                continue

            campo = ""
            novo_valor = None

            match opcao:
                case "1":
                    campo = "titulo"
                    novo_valor = input("Novo Título: ").strip()
                case "2":
                    campo = "descricao"
                    novo_valor = input("Nova Descrição: ").strip()
                case "3":
                    campo = "prioridade"
                    novo_valor = input("Nova Prioridade: ").strip()
                case "4":
                    campo = "status"
                    novo_valor = input("Novo Status: ").strip()
                case "5":
                    campo = "categoria"
                    novo_valor = input("Nova Categoria: ").strip()
                case "6":
                    campo = "prazo"
                    while True:
                        valor_prazo = input("Novo Prazo (DD/MM/AAAA): ").strip()
                        try:
                            # Converte formato BR para objeto Date do Python (que o MySQL aceita)
                            novo_valor = datetime.datetime.strptime(valor_prazo, "%d/%m/%Y").date()
                            break
                        except ValueError:
                            print("Formato de data inválido! Use DD/MM/AAAA.")
                case _:
                    print("Opção inválida!")
                    continue

            # 3. Execução do Update com dupla validação no WHERE
            if campo and (novo_valor is not None or novo_valor != ""):
                sql_update = f"UPDATE tarefas SET {campo} = %s WHERE id = %s AND usuario_id = %s"
                cursor.execute(sql_update, (novo_valor, id_tarefa, id_usuario_logado))
                conexao.commit()
                
                print(f"{campo.capitalize()} atualizado com sucesso!")
                input("\nPressione ENTER para continuar...")
                break # Sai do loop após o sucesso
            else:
                print("Alteração cancelada: valor vazio.")

        except Exception as e:
            print(f"Erro técnico ao atualizar: {e}")
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()


def deleta_tarefa(id_usuario_logado):
    while True:
        try:
            print("\n" + "="*30)
            id_input = input("Informe o ID da tarefa para ser excluída (ou 'S' para sair): ").strip()
            
            if id_input.upper() == 'S':
                break
            
            id_tarefa = int(id_input)
        except ValueError:
            print("Erro: O ID deve ser um número inteiro.")
            continue

        conexao = None
        cursor = None
        try:
            conexao = database.conectar()
            cursor = conexao.cursor(dictionary=True)

            # 1. Validação de Segurança: A tarefa existe E pertence ao usuário logado?
            sql_check = "SELECT titulo FROM tarefas WHERE id = %s AND usuario_id = %s"
            cursor.execute(sql_check, (id_tarefa, id_usuario_logado))
            tarefa = cursor.fetchone()

            if tarefa:
                print(f"\nTAREFA ENCONTRADA: {tarefa['titulo']}")
                confirmar = input(f"Tem certeza que deseja excluir permanentemente? (S/N): ").upper().strip()
                
                if confirmar == 'S':
                    # 2. Executa a deleção com dupla validação no WHERE (Garantia extra)
                    sql_delete = "DELETE FROM tarefas WHERE id = %s AND usuario_id = %s"
                    cursor.execute(sql_delete, (id_tarefa, id_usuario_logado))
                    conexao.commit()
                    
                    print(f"✅ Sucesso: Tarefa '{tarefa['titulo']}' excluída com sucesso.")
                    input("\nPressione ENTER para continuar . . .")
                    break 
                else:
                    print("Operação cancelada pelo usuário.")
                    break
            else:
                # Se não encontrar, o ID não existe ou não pertence a este usuário
                print(f"⚠️ Aviso: Não encontramos nenhuma tarefa com o ID {id_tarefa} na sua conta.")
        
        except Exception as e:
            print(f"Erro técnico ao deletar: {e}")
        
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()