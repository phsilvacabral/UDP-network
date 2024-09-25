import threading
import colorama
from datetime import datetime
from colorama import init, Fore, Back, Style
import socket

init()
init(autoreset=True)

#O Socket Python é uma biblioteca que permite a comunicação entre diferentes computadores por meio de redes.

# Variável de controle para sair do loop
sair = False

# Definindo as cores
cor_atual = colorama.Fore.BLACK  # Cor das letras
fundo_atual = colorama.Back.WHITE  # Cor de fundo

def obter_horario_atual():
    return datetime.now().strftime("%H:%M")


def recebedadoscliente(sock_cliente):
    global sair
    try:
        while not sair:
            mensagem = sock_cliente.recv(1024).decode()
            print(fundo_atual + cor_atual + mensagem + colorama.Style.RESET_ALL)
            if mensagem == "/s":
                sair = True
                break
    except (socket.error, ConnectionResetError) as e:
        print(colorama.Fore.RED + f"- ({obter_horario_atual()}) Erro ao receber mensagem do servidor: {e}. "
              + colorama.Style.RESET_ALL)


# Precisamos nos conectar no servidor
HOST = "26.177.64.196"
PORT = 9999
sock_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Cliente solicita conexão com o servidor
sock_cliente.connect((HOST, PORT))
print(colorama.Fore.BLUE + "- Chat Iniciado <-" + colorama.Style.RESET_ALL)
nome = input("- Informe seu nome para entrar no chat: ")
print("- Pressione (/s) para sair do chat")
sock_cliente.sendall(nome.encode())
#A função sendall() envia dados para um soquete conectado

# Loop via thread para receber dados do servidor
threadRecebeDados = threading.Thread(target=recebedadoscliente, args=[sock_cliente])
threadRecebeDados.start()

# Loop para enviar dados
try:
    while True:
        mensagem = input('')
        sock_cliente.sendall(mensagem.encode())
        if mensagem == "/s":
            break
finally:
    sair = True  # Sinaliza a thread para sair
    threadRecebeDados.join()  # Aguarda a thread terminar
    sock_cliente.close()
    print(colorama.Fore.YELLOW + "A conexão foi finalizada." + colorama.Style.RESET_ALL)