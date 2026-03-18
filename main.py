from menu import exibir_menu_principal
import database
def main():
    database.inicializar_banco()
    exibir_menu_principal()

if __name__ == "__main__":
    main()