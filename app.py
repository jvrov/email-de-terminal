import database as db
import getpass
from datetime import datetime

class C:
    RESET = '\033[0m'
    NEGRITO = '\033[1m'
    CINZA = '\033[90m'
    VERMELHO = '\033[91m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    CIANO = '\033[96m'
    VERDE_NEGRITO = '\033[1;92m'

def splash_screen():
    print(C.CIANO + r"Bem-vindo ao E-mail de Terminal com MongoDB" + C.RESET)

def mostrar_menu_deslogado():
    print(f"\n--- {C.NEGRITO}Menu Principal{C.RESET} ---")
    print("1. Fazer Login")
    print("2. Criar Conta")
    print("0. Sair")
    return input("Escolha: ")

def mostrar_menu_logado(email_usuario):
    nao_lidas = db.contar_nao_lidas(email_usuario)
    aviso_nao_lidas = f" ({C.VERDE_NEGRITO}{nao_lidas} não lida(s){C.RESET})" if nao_lidas > 0 else ""

    print(f"\n--- Logado como: {C.CIANO}{email_usuario}{C.RESET} ---")
    print(f"1. Ver Caixa de Entrada{aviso_nao_lidas}")
    print("2. Enviar Nova Mensagem")
    print("3. Deslogar")
    return input("Escolha: ")

def handle_login():
    print(f"\n--- {C.NEGRITO}Login{C.RESET} ---")
    email = input("E-mail: ")
    senha = getpass.getpass("Senha: ") 
    
    usuario = db.checar_login(email, senha)
    
    if usuario:
        print(f"\n{C.VERDE}Bem-vindo(a), {usuario['nome']}!{C.RESET}")
        return usuario
    else:
        print(f"\n{C.VERMELHO}[ERRO] E-mail ou senha inválidos.{C.RESET}")
        return None

def handle_criar_conta():
    print(f"\n--- {C.NEGRITO}Criar Conta{C.RESET} ---")
    nome = input("Nome completo: ")
    email = input("E-mail: ")
    senha = getpass.getpass("Senha: ")
    senha_confirma = getpass.getpass("Confirme a senha: ")

    if len(senha) < 6:
        print(f"\n{C.VERMELHO}[ERRO] A senha deve ter pelo menos 6 caracteres.{C.RESET}")
        return
    
    if senha != senha_confirma:
        print(f"\n{C.VERMELHO}[ERRO] As senhas não batem.{C.RESET}")
        return

    db.criar_usuario(nome, email, senha)

def handle_enviar_mensagem(usuario_logado):
    print(f"\n--- {C.NEGRITO}Enviar Mensagem{C.RESET} ---")
    destinatario = input("Para (e-mail): ")
    assunto = input("Assunto: ")
    corpo = input("Corpo da mensagem: ")
    
    db.enviar_mensagem(
        email_remetente=usuario_logado['email'],
        email_destinatario=destinatario,
        assunto=assunto,
        corpo=corpo
    )

def handle_ver_caixa_entrada(usuario_logado):
    print(f"\n--- {C.AMARELO}Caixa de Entrada{C.RESET} ---")
    mensagens = db.buscar_caixa_de_entrada(usuario_logado['email'])
    
    if not mensagens:
        print("Sua caixa de entrada está vazia.")
        return

    novas_mensagens_encontradas = False
    for msg in mensagens:
        data_obj = msg.get('data_envio', datetime.now()) 
        data_str = data_obj.strftime("%d/%m/%Y às %H:%M")
        
        if not msg['lida']:
            prefixo = f"{C.VERDE_NEGRITO}[NÃO LIDA]{C.RESET}"
            novas_mensagens_encontradas = True
        else:
            prefixo = f"{C.CINZA}[LIDA]{C.RESET}"

        print("-" * 40)
        print(f"{prefixo} {C.CINZA}({data_str}){C.RESET}")
        print(f"De:      {C.CIANO}{msg['de']}{C.RESET}")
        print(f"Assunto: {C.NEGRITO}{msg['assunto']}{C.RESET}")
        print(f"Corpo:   {msg['corpo']}")
        print("-" * 40)
    
    if novas_mensagens_encontradas:
        print(f"\n{C.AMARELO}Visualizando caixa de entrada...{C.RESET}")
        db.marcar_todas_como_lidas(usuario_logado['email'])
        print(f"{C.VERDE}Novas mensagens marcadas como lidas.{C.RESET}")
    
    input(f"\n{C.CINZA}Pressione ENTER para voltar ao menu...{C.RESET}")


def main():
    splash_screen()
    usuario_logado = None
    
    while True:
        try:
            if not usuario_logado:
                escolha = mostrar_menu_deslogado()
                if escolha == '1':
                    usuario_logado = handle_login()
                elif escolha == '2':
                    handle_criar_conta()
                elif escolha == '0':
                    print(f"\n{C.AMARELO}Saindo... Até mais!{C.RESET}")
                    break
                else:
                    print(f"\n{C.VERMELHO}Opção inválida.{C.RESET}")
            else:
                escolha = mostrar_menu_logado(usuario_logado['email'])
                if escolha == '1':
                    handle_ver_caixa_entrada(usuario_logado)
                elif escolha == '2':
                    handle_enviar_mensagem(usuario_logado)
                elif escolha == '3':
                    print("\nDeslogando...")
                    usuario_logado = None
                else:
                    print(f"\n{C.VERMELHO}Opção inválida.{C.RESET}")
        
        except KeyboardInterrupt:
            print(f"\n\n{C.VERMELHO}Saída forçada pelo usuário. Até mais!{C.RESET}")
            break

if __name__ == "__main__":
    main()
