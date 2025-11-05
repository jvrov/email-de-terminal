import pymongo
from passlib.hash import pbkdf2_sha256 as sha256
import re
from datetime import datetime

CONNECTION_STRING = "mongodb+srv://Cluster0:jvR301204@cluster0.8g0vn7h.mongodb.net/?appName=Cluster0"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database("db_email_terminal")
usuarios_collection = db.get_collection("usuarios")
mensagens_collection = db.get_collection("mensagens")

def criar_usuario(nome, email, senha):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print(f"\n\033[91m[ERRO] Formato de e-mail inválido. Deve ser 'usuario@dominio.com'.\033[0m")
        return False

    if usuarios_collection.find_one({"email": email}):
        print("\n\033[91m[ERRO] Este e-mail já está em uso.\033[0m")
        return False
    
    hash_senha = sha256.hash(senha)
    
    usuarios_collection.insert_one({
        "nome": nome,
        "email": email,
        "senha": hash_senha
    })
    print("\n\033[92m[SUCESSO] Usuário criado!\033[0m")
    return True

def checar_login(email, senha):
    usuario = usuarios_collection.find_one({"email": email})
    
    if not usuario:
        return None
    
    if sha256.verify(senha, usuario["senha"]):
        return usuario
    else:
        return None

def enviar_mensagem(email_remetente, email_destinatario, assunto, corpo):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email_destinatario):
        print(f"\n\033[91m[ERRO] Formato de e-mail do destinatário inválido.\033[0m")
        return False

    if not usuarios_collection.find_one({"email": email_destinatario}):
        print("\n\033[91m[ERRO] Destinatário não encontrado.\033[0m")
        return False
    
    mensagens_collection.insert_one({
        "de": email_remetente,
        "para": email_destinatario,
        "assunto": assunto,
        "corpo": corpo,
        "lida": False,
        "data_envio": datetime.now()
    })
    print("\n\033[92m[SUCESSO] Mensagem enviada!\033[0m")
    return True

def buscar_caixa_de_entrada(email_usuario):
    mensagens = mensagens_collection.find({"para": email_usuario}).sort("data_envio", -1)
    return list(mensagens)

def contar_nao_lidas(email_usuario):
    count = mensagens_collection.count_documents({
        "para": email_usuario,
        "lida": False
    })
    return count

def marcar_todas_como_lidas(email_usuario):
    mensagens_collection.update_many(
        {"para": email_usuario, "lida": False},
        {"$set": {"lida": True}}
    )
