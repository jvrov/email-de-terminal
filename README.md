# 📧 Projeto E-mail de Terminal com MongoDB

Este é um projeto de aplicação de console em Python que simula um sistema de e-mail (login, criação de conta, envio e recebimento de mensagens).

Todo o backend de dados é gerenciado por um banco de dados NoSQL **MongoDB**, hospedado na plataforma **MongoDB Atlas** (nuvem).

## ✨ Recursos

* **Autenticação Segura:** Criação de contas e login com senhas "hasheadas" (usando `passlib`).
* **Validação de Dados:** O sistema valida o formato do e-mail (ex: `deve@ter.com`) e a força da senha (mínimo de 6 caracteres).
* **Caixa de Entrada:** Visualização de mensagens recebidas, ordenadas da mais nova para a mais antiga.
* **Mensagens Lidas/Não Lidas:** O sistema mostra um contador de mensagens não lidas no menu e marca as mensagens como "LIDAS" após a visualização.
* **Interface Colorida:** Uso de códigos de escape ANSI ("fru frus") para uma interface de terminal mais amigável, com cores para sucesso, erros e informações.

## 🚀 Tecnologias Utilizadas

* **Python 3**
* **MongoDB Atlas** (Banco de dados NoSQL em nuvem)
* **`pymongo`**: O driver oficial do Python para interagir com o MongoDB.
* **`passlib`**: Para hashing e verificação de senhas de forma segura.

## ⚙️ Como Executar

1.  **Pré-requisito:** É necessário ter o `python3` e o `pip` instalados.
2.  **Configure o Banco de Dados:**
    * Crie uma conta gratuita no [MongoDB Atlas](https://cloud.mongodb.com/).
    * Crie um Cluster `M0` (Grátis).
    * Na criação do Cluster, crie um **usuário e senha** para o banco.
    * Em **"Network Access"**, libere o seu IP (clique em "Add Your Current IP Address").
3.  **Configure o Projeto:**
    * Abra o arquivo `database.py`.
    * Na linha `CONNECTION_STRING = "..."`, cole a sua string de conexão fornecida pelo Atlas, substituindo pelo seu usuário e senha corretos.
4.  **Crie o Ambiente Virtual:**
    ```bash
    python3 -m venv venv
    ```
5.  **Ative o Ambiente:**
    ```bash
    source venv/bin/activate
    ```
6.  **Instale as Dependências:**
    (Você precisará ter um arquivo `requirements.txt` com `pymongo` e `passlib` dentro)
    ```bash
    pip install pymongo passlib
    ```
7.  **Execute o Programa:**
    ```bash
    python3 app.py
    ```
