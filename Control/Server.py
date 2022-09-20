import threading
import socket
import json
from API import Api

PORT = 8080
FORMAT = 'utf-8'
HOST = "localhost"

clients = []


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        server.listen()   # Se passar listen(10), esse parametro é o numero de conexões permitidas, sem nada não tem limite
    except:
        return print('\nNão foi possivel iniciar o servidor!\n')

    while True:
        client, adress = server.accept()
        clients.append(client)

        thread = threading.Thread(target=messagesTreatment, args=[client])

        thread.start()


def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048)
            datas = getDataMsg(str(msg.decode(FORMAT)))

            print(f"Method : {datas['method']} URL : {datas['urlContent']} Body Json : {datas['bodyContent']}")
            
            # Chamar API
            api = Api()
            mandarClient = ""

            # Redirecionar rotas
            if datas["method"] == "GET":
                # Listar Clientes
                if datas['urlContent'] == "/clientes":
                    clientes = api.GET_ListaClientes()
                    mandarClient = clientes
                
                # Buscar Unico Cliente
                elif datas['urlContent'] == "/cliente":
                    cliente = api.GET_UnicoCliente(datas['bodyContent']["matricula"])
                    mandarClient = cliente
                
                # Gerar boleto para pagar
                elif datas['urlContent'] == "/gerarBoleto":
                    boletoGerado = api.GET_GerarBoleto(datas['bodyContent']["matricula"])
                    mandarClient = boletoGerado

            
            elif datas["method"] == "POST":
                # Login adm 
                if datas['urlContent'] == "/loginAdm":
                    validarAdm = api.POST_LoginAdm(datas['bodyContent']["email"], datas['bodyContent']["senha"])
                    mandarClient = validarAdm
                    
                # Login cliente
                if datas['urlContent'] == "/loginCliente":
                    validarCli = api.POST_LoginCliente(datas['bodyContent']["matricula"])
                    mandarClient = validarCli

                # Login Hidrometro
                
                if datas['urlContent'] == "/loginHidrometro":
                    validarHidro = api.POST_LoginHidrometro(datas['bodyContent']["matricula"])
                    mandarClient = validarHidro
                pass
            
            elif datas["method"] == "PUT":
                # Bloquar Hidrometro
                if datas['urlContent'] == "/cliente/bloquear":
                    blockHidro = api.PUT_BloquearHidrometro(datas['bodyContent']["matricula"])
                    mandarClient = blockHidro
                # Pagar conta
                elif datas['urlContent'] == "/pagarConta":
                    pagConta = api.PUT_Pagarconta(datas['bodyContent']["matricula"])
                    mandarClient = pagConta

                # Setar novo consumo total do hidrometro
                elif datas['urlContent'] == "/madarDadosHidrometro":
                    mat = datas['bodyContent']["matricula"]
                    novoConsumo = datas['bodyContent']["novoConsumo"]
                    vazando = datas['bodyContent']["vazamento"]
                    pagConta = api.PUT_NovoConsumoTotal(mat, novoConsumo, vazando)
                    mandarClient = pagConta
            
            # Resultado da API manda pro broadCast
            # Pegar a url e mandar para sua rota Especifica.
            
            # Como já vem com Dumps da API, não precisa faze novamente
            broadcast(mandarClient, client)
        except:
            deleteClient(client)
            break


def broadcast(msg, client):
    for clientItem in clients:
        #if clientItem != client:
        if clientItem == client:
            try:
                clientItem.send(msg.encode(FORMAT))
            except:
                deleteClient(clientItem)
                

def deleteClient(client):
    clients.remove(client)


def getDataMsg(msg):
    """
        Metodo para divir as informações que vem na requisição e retornar apenas,
        o metodo da requisição ou o verbo HTTP usado
        o conteudo da URL
        o conteudo em Json 
    """
    method = msg.split(" ")[0]
    urlContent = msg.split(" ")[1]
    bodyContent = ""
   
    try:    
        msg = msg.replace("{","{dir") 
        msg = msg.replace("}","esq}")
        msg = msg.split("{")[1].split("}")[0]
        msg = msg.replace("dir","{")
        msg = msg.replace("esq","}")

        bodyContent = json.loads(msg)

    except:
        bodyContent = "{}"

    return {"method" : method, "urlContent" : urlContent, "bodyContent" : bodyContent}

main()