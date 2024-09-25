import threading
from datetime import datetime
import colorama
from colorama import init
init(autoreset=True)
lista_cliente = []
import socket


#cd (change directory) comando para cmd

fundo_atual = colorama.Back.WHITE  # Cor de fundo

def obter_horario_atual():
    return datetime.now().strftime("%H:%M")


# Recebe dados do cliente


def recebedados(conn, ender):
    try:
        nome = conn.recv(50).decode() # O decode() é usado para decodificar os bytes recebidos em uma string, utilizando a codificação padrão (geralmente UTF-8) para converter os dados recebidos em um formato legível.
        print(fundo_atual + colorama.Fore.GREEN + f"- Conexão com o {nome} - {ender[0]}:{ender[1]} foi iniciada as "
                             f"{obter_horario_atual()}. ___" + colorama.Style.RESET_ALL)
        mensagementrou = f"-> {nome} entrou no chat as {obter_horario_atual()}! <-"
        broadcast(mensagementrou)
        while True:
            mensagem = conn.recv(1024).decode()
            if mensagem == "/s":
                mensagemsaida = f"- {nome} saiu do chat as {obter_horario_atual()}! <-"
                print(fundo_atual + colorama.Fore.GREEN + f"- Conexão com o {nome} - {ender[0]}:{ender[1]} foi finalizada as "
                      f"{obter_horario_atual()}. -" + colorama.Style.RESET_ALL)
                lista_cliente.remove(conn)
                conn.close()
                broadcast(mensagemsaida)
                break
            mensagemnome = f"{obter_horario_atual()}: {nome} -> {mensagem}"
            print(fundo_atual + colorama.Fore.YELLOW + mensagemnome + colorama.Style.RESET_ALL)
            broadcast(mensagemnome)

    except Exception as e:
        print(fundo_atual  + colorama.Fore.RED + f"- ({obter_horario_atual()}) Erro ao processar conexão com {nome}: {e}. _-_"
              + colorama.Style.RESET_ALL)
        lista_cliente.remove(conn)
        conn.close()
        mensagemsaida = f"- {nome} saiu do chat devido a um erro as {obter_horario_atual()}! <-"
        broadcast(mensagemsaida)


# Envia os dados para todos os clientes


def broadcast(mensagem):
    for cliente in lista_cliente:
        try:
            cliente.sendall(mensagem.encode())
        except Exception as e:
            print(fundo_atual + colorama.Fore.RED + f"- ({obter_horario_atual()}) Erro ao enviar mensagem para cliente: {e}. <-"
                  + colorama.Style.RESET_ALL)
            # Remova a conexão da lista se ocorrer um erro
            lista_cliente.remove(cliente)


# Criação do socket e das informações do servidor
HOST = "26.177.64.196"
PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
print(fundo_atual + colorama.Fore.GREEN + f"- O servidor {HOST}:{PORT} foi ativado as "
                     f"{obter_horario_atual()} e no aguardo de conexões. <-" + colorama.Style.RESET_ALL)

# Loop para aceitar novas conexões
while True:
    try:
        conn, ender = sock.accept()
        lista_cliente.append(conn)
        # Loop via thread para receber dados do cliente
        threadCliente = threading.Thread(target=recebedados, args=[conn, ender])
        threadCliente.start()
    except Exception as e:
        print(fundo_atual + colorama.Fore.RED + f"- ({obter_horario_atual()}) Erro ao aceitar conexão: {e}. <-" + colorama.Style.RESET_ALL)
        break
