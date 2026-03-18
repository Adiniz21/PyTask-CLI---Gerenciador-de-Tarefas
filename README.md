# 🎯 PyTask CLI - Gerenciador de Tarefas

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql&logoColor=white)
![API](https://img.shields.io/badge/API-ViaCEP-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen?style=for-the-badge)

---

## 📌 Sobre o Projeto

Este projeto consiste no desenvolvimento de um **gerenciador de tarefas via linha de comando (CLI)** em Python, com armazenamento de dados em banco relacional (**MySQL**) e integração com a **API ViaCEP**.

O sistema registra os usuários, automatiza o preenchimento de endereços e permite gerenciar tarefas de forma segura e individual, garantindo que cada usuário acesse apenas as suas próprias informações.

O projeto foi desenvolvido com foco em aprendizado prático e consolidação de conhecimentos, envolvendo:

* lógica de programação
* integração e manipulação de banco de dados (CRUD)
* consumo de APIs REST e manipulação de JSON
* segurança da informação (Hashing de senhas)
* organização modular de código estruturado

---

## 🚀 Funcionalidades

### 👤 Sistema de Usuários
Cadastro e login de usuários de forma segura. As senhas são protegidas com criptografia (`bcrypt`). O sistema permite que o usuário edite suas informações de perfil (nome, e-mail, senha) ou exclua sua conta permanentemente (deletando em cascata todas as tarefas e endereços vinculados).

### 📍 Automação de Endereços
Durante o cadastro ou na atualização do perfil, o usuário precisa informar apenas o CEP. O sistema consome a API RESTful do ViaCEP para buscar e salvar automaticamente o logradouro, bairro, cidade e estado.

### 📋 Gestão de Tarefas (CRUD)
Menu dedicado para o usuário adicionar, listar, editar e deletar suas tarefas. O sistema armazena informações detalhadas para cada registro:
* Título e Descrição
* Prioridade e Status
* Categoria
* Prazo de entrega (com validação de formato de data)

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Banco de Dados:** MySQL
* **Bibliotecas Externas:**
  * `mysql-connector-python`: Driver de comunicação com o banco.
  * `bcrypt`: Geração de hash seguro para as senhas.
  * `requests`: Requisições HTTP para a API do ViaCEP.
* **Bibliotecas Nativas:** `datetime` (manipulação de datas) e `os` (limpeza de terminal).

---

## ⚙️ Como executar o projeto

### Pré-requisitos
* [Python 3.x](https://www.python.org/downloads/) instalado.
* [MySQL Server](https://dev.mysql.com/downloads/mysql/) rodando localmente.

### 1. Clonar o repositório
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```
### 2. Criar e ativar o Ambiente Virtual

#### Criar ambiente
python -m venv venv

#### Ativar no Windows
venv\Scripts\activate

#### Ativar no Linux/Mac
source venv/bin/activate

### 3. Instalar dependências
```
pip install mysql-connector-python bcrypt requests
```

### 4. Configurar o Banco de Dados
```
DB_CONFIG = {
    "host": "localhost",
    "user": "root",       # Altere se necessário
    "password": "root123" # Altere se necessário
}
```

### 5. Iniciar a aplicação
```
python main.py
```
---

## 📁 Arquitetura do Sistema

| Arquivo | Descrição |
| :--- | :--- |
| `main.py` | Ponto de entrada. Orquestra a inicialização do banco de dados e o menu principal. |
| `menu.py` | Responsável pela interface de linha de comando (CLI) e roteamento visual das opções. |
| `database.py` | Gerencia a conexão com o MySQL e a criação automatizada do banco e das tabelas. |
| `config.py` | Centraliza variáveis globais de configuração (Nome do banco de dados, URL de APIs). |
| `usuario.py` | Encapsula a lógica de autenticação, edição de perfil e criptografia de senhas. |
| `endereco.py` | Gerencia a integração com a API ViaCEP e a persistência dos dados de localização. |
| `tarefa.py` | Contém as regras de negócio para o CRUD de tarefas, incluindo a validação de datas. |
