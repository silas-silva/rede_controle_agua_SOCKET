import json
import threading
import socket
from time import sleep

PORT = 8080
FORMAT = 'utf-8'
HOST = "localhost"


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((HOST, PORT))          # Tentando se conectar ao servidor
    except:
        return print('\nNão foi possivel se conectar ao servidor\n')

    email_validacao = validarADM(client)
    email = email_validacao[0]
    validado = email_validacao[1]

    if validado == True:
        print('\nConectado')
        thread1 = threading.Thread(target=receiveMessages, args=[client])
        thread2 = threading.Thread(target=sendMessages, args=[client, email])
        thread1.start()
        thread2.start()



def validarADM(client):
    # metodo para validar se o adm existe na base de dados
    # Pedir email e senha para o adm
    
    email = input('Email> ')
    
    while email == "":
        email = input('Email> ')
    
    senha = input('Senha> ')
    
    while senha == "":
        senha = input('Senha> ')

    # Mandar esses dados para o servidor Validar
    DadoFormatado = 'POST /loginAdm {"email" : "-", "senha" : "_" }'.replace("-",email).replace("_",senha)
    client.send(DadoFormatado.encode(FORMAT))

    # Verificar o retorno do servidor e caso seja falso, parar o client atual
    # Response server é um Json
    responseServer = client.recv(2048).decode(FORMAT)
    responseServer = json.loads(responseServer)
        
    if responseServer[14:18] == "True":
        pass
    else:
        print("ADM não encontrado")
        input("Aperte enter para sair ....")
        client.close()
        return (False, False)

    return (email, True)
 


def receiveMessages(client):
    # Metodo que recebe as mensagens vindas do servidor
    while True:
        try:
            msg = client.recv(2048).decode(FORMAT)
            msg = json.loads(msg)
            print(msg + '\n')
            #Controlar Hidrometro por aqui

            # Fazer Opção de bloquear o hidrometro pelo dado vindo do servidor
        except:
            print('\nNão foi possivel permanecer conectado no servidor\n')
            print('Digite o número < 1 > e Pressione <Enter> para continuar')
            client.close()
            break


def sendMessages(client, userName):
    while True:
        try:
            #Fazer Menu de controle do Hidrometro aqui
            # Sleep para esperar um tempo para receber a resposta do Receive Messages
            sleep(2)
            print("===============  MENU  ===================")
            print("[ 1 ] LISTAR CLIENTES")
            print("[ 2 ] PEGAR DADOS DE UM CLIENTE")
            print("[ 3 ] BLOQUEAR HIDROMETRO DO CLIENTE")
            print("[ 4 ] SAIR")
            escolha = input("... ")

            while escolha != "1" and escolha != "2" and escolha != "3" and escolha != "4":
                escolha = input("... ") 



            requisicao = ""

            if escolha == "1":
                requisicao = f'GET /clientes'
            elif escolha == "2":
                matricula = input("MATRICULA DO CLIENTE: ")
                dic = { "matricula" :  matricula}
                requisicao = f'GET /cliente {json.dumps(dic)}'
            elif escolha == "3":
                matricula = input("MATRICULA DO CLIENTE: ")
                dic = { "matricula" :  matricula}
                requisicao = f"PUT /cliente/bloquear {json.dumps(dic)}"
            elif escolha == "4":
                client.close()
                return

            # Fazer ifs para controlar mudanças na classe Hidrometro ou enviar dados para o server.
            client.send(f'{requisicao}'.encode(FORMAT))
        except:
            return


main()