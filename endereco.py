import config
import database 
import requests

def altera_endereco(id):
    while True:
        cep = input("Informe o CEP: ").strip().replace("-", "") # Limpa o CEP
        url = config.URL_API_VIA_CEP.format(cep = cep)
        
        try:
            resposta = requests.get(url)
            if resposta.status_code != 200:
                print("Erro ao consultar API. Tente novamente.")
                continue
            
            dados = resposta.json()
            if "erro" in dados:
                print("CEP inválido, tente novamente.")
                continue
            conexao = database.conectar()
            cursor = conexao.cursor(dictionary=True)
            
            sql_check = "SELECT cep FROM endereco WHERE usuario_id = %s"
            cursor.execute(sql_check, (id,))
            resultado = cursor.fetchone()
            
            if resultado and resultado['cep'].replace("-", "") == cep:
                print("Já é esse o endereço que está salvo. Tente outro.")
                continue 
            
            sql_update = "UPDATE endereco SET cep = %s, logradouro = %s, bairro = %s, cidade = %s, estado = %s WHERE usuario_id = %s"
            values = (dados["cep"], dados["logradouro"], dados["bairro"], dados["localidade"], dados.get("uf", dados.get("estado")), id)
            
            cursor.execute(sql_update, values)
            conexao.commit()
            
            print("Endereço atualizado com sucesso!")
            input("Pressione ENTER para continuar . . .")
            break

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            input("Pressione ENTER para tentar novamente...")
        
        finally:
            if 'conexao' in locals() and conexao:
                cursor.close()
                conexao.close()