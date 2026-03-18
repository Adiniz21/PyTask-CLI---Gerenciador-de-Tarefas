import database
import bcrypt 
import requests
import config
import menu

def cadastro_usuario():
    try:
        conexao = database.conectar()
        cursor = conexao.cursor(dictionary=True)

        print("Conectou com sucesso!")

        nome_usuario = input("Insira o seu nome por favor: ")
        while True:
            email_usuario = input("Insira o seu email por favor: ")

            sql = "SELECT * FROM usuarios WHERE email = %s"
            values = (email_usuario,)

            cursor.execute(sql, values)
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                print("Já existe um usuário cadastrado com esse email. Tente outro.")
            else:
                break

        while True:
            senha_usuario = input("Insira a sua senha por favor: ")
            if len(senha_usuario) < 8:
                print("A senha deve ter no mínimo 8 dígitos")
            else:
                break

        senha_hash = bcrypt.hashpw(
            senha_usuario.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        sql = """
        INSERT INTO usuarios (nome, email, senha_hash, data_criacao)
        VALUES (%s, %s, %s, NOW())
        """

        values = (nome_usuario, email_usuario, senha_hash)

        cursor.execute(sql, values)
        conexao.commit()

        usuario_id = cursor.lastrowid

        while True:
            cep = input("Informe o CEP: ").strip()
            url = config.URL_API_VIA_CEP.format(cep=cep)

            resposta = requests.get(url)

            if resposta.status_code == 200:
                dados = resposta.json()

                if "erro" in dados:
                    print("CEP inválido, tente novamente.")
                else:
                    break
            else:
                print("Erro ao consultar API. Tente novamente.")

        sql = """
                INSERT INTO endereco (usuario_id, cep, logradouro, bairro, cidade, estado, data_criacao)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """
        values = (usuario_id, dados["cep"], dados["logradouro"], dados["bairro"], dados["localidade"], dados["estado"])

        cursor.execute(sql, values)
        conexao.commit()        


        print("Usuário cadastrado com sucesso!")

        cursor.close()
        conexao.close()

    except Exception as erro:
        print("Erro ao cadastrar usuário:", erro)


def Login():
    try:
        print("Para fazer o Login dentro do sistema por favor insira a o seu E-mail e a sua senha.")
        conexao = database.conectar()
        cursor = conexao.cursor(dictionary=True)
        while True:
            email_usuario = input("Insira o seu E-mail por favor: ")
            sql = "SELECT * FROM usuarios WHERE email = %s"
            values = (email_usuario,)

            cursor.execute(sql, values)
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                break
            else:
                print("E-mail inexistente. Tente novamente.")
        
        while True:
            senha_usuario = input("Insira a senha por favor: ")
            
            # 1. Busca o hash que já existe no banco de dados
            sql = "SELECT * FROM usuarios WHERE email = %s"
            values = (email_usuario,)
            cursor.execute(sql,values)            
            
            resultado = cursor.fetchone() # Pega a linha encontrada
                        
            if resultado:
                senha_hash_bd = resultado['senha_hash'] # O hash vindo do banco (em bytes ou string)
                                
                # O bcrypt precisa de bytes, então garantimos a conversão se necessário
                if isinstance(senha_hash_bd, str):
                    senha_hash_bd = senha_hash_bd.encode('utf-8')

                # 2. A MÁGICA: checkpw compara a senha digitada com o hash do banco
                    if bcrypt.checkpw(senha_usuario.encode("utf-8"), senha_hash_bd):
                        print("Senha correta! Acesso liberado.")
                        id = resultado['id']
                        cursor.close()
                        conexao.close()
                        menu.menu_usuario_logado(id, email_usuario)
                        break                        
                    else:
                        print("Senha incorreta. Tente novamente.")
                else:
                    print("Usuário não encontrado.")
                    break
            


    except:
        print("Erro ao fazer login do usuário.")


def excluir(id):
    while True:
        escolha = input("Você tem certeza que deseja excluir o seu usuário? S/N")    
        match escolha.strip().lower():
            case "s":
                try:
                    conexao = database.conectar()
                    cursor = conexao.cursor(dictionary=True)

                    sql = "DELETE FROM tarefas WHERE usuario_id = %s"
                    values = (id,)
                    cursor.execute(sql, values)

                    sql = "DELETE FROM endereco WHERE usuario_id = %s"
                    values = (id,)
                    cursor.execute(sql, values)

                    sql = "DELETE FROM usuarios WHERE id = %s"
                    values = (id,)
                    cursor.execute(sql, values)
                    conexao.commit()
                    print("\nSua conta e todos os seus dados foram excluídos com sucesso!")
                    
                    cursor.close()
                    conexao.close()

                    input("Pressione Enter para continuar . . .")
                    return "sim"
                except:
                    print("Erro ao excluir usuário")
            case "n":
                print("Não")
                return "nao"
            case _:
                print("Escolha um opção válida")

def altera_usuario(id):
    while True:
        print("Escolha uma opção para alterar o seu usário")
        print("1 - Alterar E-mail")
        print("2 - Alterar nome")
        print("3 - Alterar senha")
        print("4 - Voltar para menu principal")

        try:
            escolha = int(input("Insira a sua opção: "))
        except ValueError:
            print("Escolha um opção válida")
            input("Pressione ENTER para continuar...")
            continue

        match escolha:
            case 1:
                while True:
                    novo_email = input("Insira o novo email: ")
                    if "@" not in novo_email:
                        print("E-mail inválido.")
                    else:
                        try:
                            conexao = database.conectar()
                            cursor = conexao.cursor(dictionary=True)
                            sql = "SELECT * FROM usuarios WHERE email = %s"
                            values = (novo_email,)

                            cursor.execute(sql, values)
                            usuario_existente = cursor.fetchone()

                            if usuario_existente:
                                print("Já existe um usuário cadastrado com esse email. Tente outro.")
                            else:
                                sql = "UPDATE usuarios SET email = %s WHERE id = %s"
                                values = (novo_email.strip(), id)
                                cursor.execute(sql, values)
                                conexao.commit()
                                print("E-mail alterado com sucesso")
                                input("Digite Enter para continuar . . .")
                                cursor.close()
                                conexao.close()
                                break
                        except:
                            print("Erro ao alterar E-mail.")

            case 2:
                while True:
                    novo_nome_usuario = input("Informe o novo nome: ")
                    if len(novo_nome_usuario) < 3:
                        print("Insira um nome real")
                    else:
                        try:
                            conexao = database.conectar()
                            cursor = conexao.cursor(dictionary=True)
                            sql = "UPDATE usuarios SET nome = %s WHERE id = %s"
                            values = (novo_nome_usuario, id)
                            cursor.execute(sql, values)
                            conexao.commit()
                            print("Nome alterado com sucesso")
                            input("Digite ENTER para continuar . . .")
                            cursor.close()
                            conexao.close()
                            break
                        except:
                            print("Erro ao alterar nome do usuário, tente novamente.")
            
            case 3:
                while True:
                    nova_senha = input("Insira a nova senha: ")
                    if len(nova_senha)<8:
                        print("A senha deve ter no mínimo 8 dígitos")
                    else:
                        try:
                            conexao = database.conectar()
                            cursor = conexao.cursor(dictionary=True)
                            senha_hash = bcrypt.hashpw(
                                nova_senha.encode("utf-8"),
                                bcrypt.gensalt()
                            ).decode("utf-8")
                            sql = "UPDATE usuarios SET senha_hash = %s where id = %s"
                            values = (senha_hash, id)
                            cursor.execute(sql, values)
                            conexao.commit()
                            print("Senha alterada com sucesso!")
                            input("Aperte ENTER para continuar . . .")
                            cursor.close()
                            conexao.close()
                            break
                        except:
                            print("Erro ao alterar Senha")

            case 4:
                input("Pressione ENTER para continuar . . .")
                break
            
            case _:
                print('Informe uma opção válida.')