import json
import threading
import socket
import sys
from time import sleep

sys.path.append('../Model')
from HidrometroModel import Hidrometro

PORT = 8080
FORMAT = 'utf-8'
HOST = "localhost"

hidro = Hidrometro()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((HOST, PORT))          # Tentando se conectar ao servidor
    except:
        return print('\nNão foi possivel se conectar ao servidor\n')
    

    validarHidrometro(client)

    matriculaHidrometro = "" # Pegar essa matricula do Objeto Hidrometro

    
    print('\nConectado')
    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, matriculaHidrometro])
    thread3 = threading.Thread(target=sendDataHidro, args=[client])
    
    thread1.start()
    thread2.start()
    thread3.start()



def validarHidrometro(client):
    # Metodo para validar se o hidrometro já existe na base de dados
    # Se existir, só pegar os dados, se não, criar um
    
    matricula = input('Matricula> ')

    while matricula == "":
        matricula = input('Matricula> ')

    hidro.matricula = matricula

    # Mandar esses dados para o servidor Validar
    DadoFormatado = 'POST /loginHidrometro  {"matricula" : "-" }'.replace("-",matricula)
    client.send(DadoFormatado.encode(FORMAT))

    # Verificar o retorno do servidor e caso seja falso, parar o client atual
    # ResponseServer é o retorno com os dados do Hidrometro, e vai ser um Json
    responseServer = client.recv(2048).decode(FORMAT)
    
    print(json.loads(responseServer))
        
 


def receiveMessages(client):
    # Metodo que recebe as mensagens vindas do servidor
    while True:
        try:
            msg = client.recv(2048).decode(FORMAT)
            # hidroEstado
            #{"validar" : "Existe", "consumoAtual" : "-"}
            print(msg + '\n')
            #Controlar Hidrometro por aqui

            # Fazer Opção de bloquear o hidrometro pelo dado vindo do servidor
        except:
            print('\nNão foi possivel permanecer conectado no servidor\n')
            print('Pressione < 1 > e depois <Enter> para continuar')
            client.close()
            quit()


def sendMessages(client, userName):
    while True:
        try:
            #Fazer Menu de controle do Hidrometro aqui
            # Sleep para esperar um tempo para receber a resposta do Receive Messages
            sleep(2)
            print("===============  MENU  ===================")
            print(f" ===== CONSUMO TOTAL {hidro.consumo} M³ ======")
            print(f" ===== VAZÃO ATUAL {hidro.vazao} M³/S ======")
            print("[ 1 ] AUMETNAR VAZÃO EM 1 M³/S ")
            print("[ 2 ] DIMINUIR VAZÃO EM 1 M³/S ")
            escolha = input("... ")

            while escolha != "1" and escolha != "2":
                escolha = input("... ")

            if escolha == "1":
                hidro.aumentarVazao()
            elif escolha == "2":
                hidro.diminuirVazao()

        except:
            return


def sendDataHidro(client):
    segundos = 0
    while True:
        try:
            sleep(1)
            if hidro.bloqueado == False:
                hidro.consumo += hidro.vazao
            
            elif hidro.bloqueado == True:
                # Quando o hidrometro bloqueado, mandar dados para o servidor de 3 em 3 segundos
                sleep(3)
                requisicao = 'PUT /madarDadosHidrometro { "matricula" : "_" , "novoConsumo" : "-"}'.replace("_", hidro.matricula).replace("-", str(hidro.consumo))
                segundos = 0 # Resetar os segundos
                client.send(f'{requisicao}'.encode(FORMAT))
            
            if segundos >= 5 and hidro.bloqueado == False:
                # de 10 em 10 segundos mandar os dados para o servidor caso o hidrometro não esteja bloqueado
                requisicao = 'PUT /madarDadosHidrometro {"matricula" : "_" , "novoConsumo" : "-"}'.replace("_", hidro.matricula).replace("-", str(hidro.consumo))
                segundos = 0 # Resetar os segundos
                client.send(f'{requisicao}'.encode(FORMAT))
            
            segundos += 1
        except:
            client.close()
            return

main()