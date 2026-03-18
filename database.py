import mysql.connector
import config

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root123"
}

DB_NAME = config.NOME_BANCO


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database=DB_NAME
    )


def criar_banco():
    conexao = mysql.connector.connect(**DB_CONFIG)
    cursor = conexao.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

    cursor.close()
    conexao.close()


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(150) NOT NULL UNIQUE,
        senha_hash VARCHAR(255) NOT NULL,
        data_criacao DATETIME
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS endereco (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT,
        cep VARCHAR(10),
        logradouro VARCHAR(150),
        bairro VARCHAR(150),
        cidade VARCHAR(150),
        estado VARCHAR(150),
        data_criacao DATETIME,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT,
        endereco_id INT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        prioridade TEXT NOT NULL,
        status TEXT NOT NULL,
        categoria TEXT NOT NULL,
        data_criacao DATETIME,
        prazo DATETIME,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (endereco_id) REFERENCES endereco(id)
    )
    """)

    conexao.commit()

    cursor.close()
    conexao.close()


def inicializar_banco():
    criar_banco()
    criar_tabelas()