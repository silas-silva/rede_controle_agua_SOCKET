import json
import threading
import socket
from time import sleep

PORT = 8080
FORMAT = 'utf-8'
HOST = "172.16.103.8"


def main():
    # Criar o cliente e se conectar com o servidor
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((HOST, PORT))          # Tentando se conectar ao servidor
    except:
        return print('\nNão foi possivel se conectar ao servidor\n')

    matricula_validacao = validarCliente(client)

    matricula = matricula_validacao[0]
    validado = matricula_validacao[1]

    if validado == True:
        print('\nConectado')
        thread1 = threading.Thread(target=receiveMessages, args=[client])
        thread2 = threading.Thread(target=sendMessages, args=[client, matricula])
        thread1.start()
        thread2.start()


def validarCliente(client):
    """ metodo para validar se o cliente existe na base de dados

        Args:
            client: objeto de conexão do cliente
        
        Returns:
            Json: Json contendo a matricula e um boolean se o cliente existe
    """

    # Pedir matricula
    print("===== Cliente =====")
    matricula = input('Matricula> ')

    while matricula == "":
        matricula = input('Matricula> ')

    # Mandar esses dados para o servidor Validar
    DadoFormatado = 'POST /loginCliente {"matricula" : "-"}'.replace("-",matricula)
    client.send(DadoFormatado.encode(FORMAT))

    # Verificar o retorno do servidor e caso seja falso, parar o client atual
    # Response server é um Json
    responseServer = client.recv(2048).decode(FORMAT)
    responseServer = json.loads(responseServer)    

    if responseServer[15:19] == "True":
        pass
    else:
        print("Cliente não encontrado")
        input("Aperte enter para sair ....")
        client.close()
        return (False, False)

    return (matricula, True)
 

def receiveMessages(client):
    """ Metodo que recebe as mensagens vindas do servidor

        Args:
            client: objeto de conexão do adm
    """
    # Metodo que recebe as mensagens vindas do servidor
    while True:
        try:
            msg = client.recv(2048).decode(FORMAT)  
            try:           
                print(json.loads(msg + '\n'))
            except:
                print(msg + '\n')
        except:
            print('\nNão foi possivel permanecer conectado no servidor\n')
            print('Pressione <Enter> para continuar')
            client.close()
            break


def sendMessages(client, matricula):
    """ metodo para enviar mensagem para o servidor

        Args:
            matricula (str): matricula do cliente
            client: objeto de conexão do cliente
    """
    while True:
        try:
            #Fazer Menu de controle do Cliente aqui
            # Sleep para esperar um tempo para receber a resposta do Receive Messages
            sleep(2)
            print("===============  MENU  ===================")
            print("[ 1 ] GERAR BOLETO")
            print("[ 2 ] PAGAR CONTA")
            print("[ 3 ] SAIR")
            escolha = input("... ")

            while escolha != "1" and escolha != "2" and escolha != "3":
                escolha = input("... ") 

            requisicao = ""
            dicMat = { "matricula" :  matricula}

            if escolha == "1":
                requisicao = f'GET /gerarBoleto {json.dumps(dicMat)}'
            elif escolha == "2":
                requisicao = f"PUT /pagarConta {json.dumps(dicMat)}"
            elif escolha == "3":
                client.close()
                return

            client.send(f'{requisicao}'.encode(FORMAT))
        except:
            return


main()