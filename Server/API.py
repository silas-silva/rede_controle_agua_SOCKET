# -*- coding: utf-8 -*-

import json

class Api:
    

    # Metodos de Login


    def POST_LoginAdm(self, email, senha):
        # Passado o Email e senha, retorna se o adm existe
        # Ler arquivo
        with open("banco/adms.json", 'r' , encoding='utf-8') as database:
            adms = json.load(database)
        
        print("====================== ADM ==========================")
        print(adms)
        print("=====================================================")

        # Verificar se o email existe
        if email.lower() in adms:
            # Verificar se a senha corresponde
            if adms[email.lower()]["senha"].rstrip() == str(senha).rstrip():
                return json.dumps('{"validar" : "True"}') # Retornar validação verdadeira
            else:
                return json.dumps('{"validar" : "False"}') # Retornar validação falsa
        else:
            return json.dumps('{"validar" : "False"}') # Retornar validação falsa


    def POST_LoginHidrometro(self, matricula):
        # Ler dados do banco
       
        with open("banco/hidrometros.json", 'r' , encoding='utf-8') as database:
            hidrometros = json.load(database)
        
        # Verificar se a matricula existe
        if matricula.lower() in hidrometros:
            consumoAtual = hidrometros[matricula.lower()]["consumoAtual"]
            bloq = hidrometros[matricula.lower()]["bloqueado"]
            retorno = '{"Hidrometro" : "Já Existia", "consumoAtual" : "-", "bloqueado" : "_"}'.replace("-", str(consumoAtual)).replace("_", str(bloq))
            return json.dumps(retorno) # Retornar validação existente e quanto o hidrometro consumiu até o momento
        
        else:
            # Adicionar novo hidrometro
            hidrometros[matricula.lower()] = {"ultimoConsumo" : "0", "consumoAtual" : "0", "bloqueado" : "0", "vazando" : "0"}
            
            #Salvar alterações no banco
            with open("banco/hidrometros.json", 'w' , encoding='utf-8') as database:
                json.dump(hidrometros, database, indent=4)   
            
            # adicionar Cliente
            self.POST_NovoCliente(matricula)

            # Retornar 
            retorno = '{"Hidrometro" : "Foi Criado", "consumoAtual" : "0", "bloqueado" : "0"}'  # Consumo atual é 0, pois não foi criado agora
            return json.dumps(retorno) # Retornar validação existente e quanto o hidrometro consumiu até o momento
    

    def POST_LoginCliente(self, matricula):
        # Ler dados do banco
       
        with open("banco/clientes.json", 'r' , encoding='utf-8') as database:
            clientes = json.load(database)
        
        # Verificar se a matricula existe
        if matricula.lower() in clientes:
            return json.dumps('{ "validar" : "True"}') # Retornar validação existente e quanto o hidrometro consumiu até o momento
        
        else:
            return json.dumps('{ "validar" : "False"}') # Retornar validação existente e quanto o hidrometro consumiu até o momento


    # Metodos ADM


    def GET_ListaClientes(self):
        # Retornar matriculas dos clientes
        
        try:
            # Pegar dados do banco
            with open("banco/clientes.json", 'r' , encoding='utf-8') as database:
                clientes = json.load(database)
            
            jsonMandar = '{ "Clientes" : '

            for v , k in clientes.items():
                jsonMandar += f' "{v}",'

            jsonMandar = jsonMandar.rstrip(',')
            jsonMandar += " }"
        except:
            jsonMandar = '{ "Clientes" : "Nenhum" }'

        return json.dumps(jsonMandar)
        
        
    def GET_UnicoCliente(self, matricula):
        # Com a matricula do cliente, vai retornar os dados do mesmo
        try:
            # Pegar dados do banco
            with open("banco/clientes.json", 'r' , encoding='utf-8') as database:
                clientes = json.load(database)

            with open("banco/hidrometros.json", 'r' , encoding='utf-8') as database:
                hidrometros = json.load(database)

            if matricula in clientes:
                divida = clientes[matricula]["divida"]
                retorno = '{"validar" : "True", "Divida" : "-", "vazando" : "_" }'.replace("-", str(divida)).replace("_", hidrometros[matricula]["vazando"])
                return json.dumps(retorno)
            else:
                return json.dumps('{ "validar" : "False" }')
        except:
            return json.dumps('{ "validar" : "False" }')



    def PUT_BloquearHidrometro(self, matricula):
        # Mandar um dado de block para o hidrometro do cliente, tratar no servidor para mandar apenas para o cliente especifico
        
        #
        # Fazer uma validação para ver se o cliente deve
        #
        try:
            # Pegar dados do banco
            with open("banco/hidrometros.json", 'r' , encoding='utf-8') as database:
                hidrometros = json.load(database)
            
            if matricula in hidrometros:
                # bloquar hidrometro
                uc = str(hidrometros[matricula.lower()]["ultimoConsumo"])
                ca = str(hidrometros[matricula.lower()]["consumoAtual"])
                va = str(hidrometros[matricula.lower()]["vazando"])
                hidrometros[matricula.lower()] = {"ultimoConsumo" : uc, "consumoAtual" : ca, "bloqueado" : "1", "vazando" : va}
            
                #Salvar alterações no banco
                with open("banco/hidrometros.json", 'w' , encoding='utf-8') as database:
                    json.dump(hidrometros, database, indent=4)  
                return json.dumps('{ "validar" : "True" , "bloqueado" : "1" }')
            else:
                return json.dumps('{ "validar" : "False" }')
        except:
            return json.dumps('{ "validar" : "False" }')


    def PUT_DesbloquearHidrometro(self, matricula):
        # Mandar um dado para tirar block para o hidrometro do cliente, tratar no servidor para mandar apenas para o cliente especifico
        try:
            # Pegar dados do banco
            with open("banco/hidrometros.json", 'r' , encoding='utf-8') as database:
                hidrometros = json.load(database)

            if matricula in hidrometros:
                # bloquar hidrometro
                uc = str(hidrometros[matricula.lower()]["ultimoConsumo"])
                ca = str(hidrometros[matricula.lower()]["consumoAtual"])
                va = str(hidrometros[matricula.lower()]["vazando"])
                hidrometros[matricula.lower()] = {"ultimoConsumo" : uc, "consumoAtual" : ca, "bloqueado" : "0", "vazando" : va}
            
                #Salvar alterações no banco
                with open("banco/hidrometros.json", 'w' , encoding='utf-8') as database:
                    json.dump(hidrometros, database, indent=4)  
                return json.dumps('{ "validar" : "True" , "bloqueado" : "0" }')
            else:
                return json.dumps('{ "validar" : "False" }')
        except:
            return json.dumps('{ "validar" : "False" }')
    


    # Metodos Cliente

    def POST_NovoCliente(self, matricula):
        # Criar novo cliente ao ser criado um hidrometro
        # Ler dados do banco
       
        with open("banco/clientes.json", 'r' , encoding='utf-8') as database:
            clientes = json.load(database)
        
        # Adicionar novo cliente
        clientes[matricula.lower()] = {"divida" : "0"}
        
        #Salvar alterações no banco
        with open("banco/clientes.json", 'w' , encoding='utf-8') as database:
            json.dump(clientes, database, indent=4)   


    def GET_GerarBoleto(self, matricula):
        # Fazez consulta no banco, e gerar conta para o cliente
        with open("banco/clientes.json", 'r' , encoding='utf-8') as database:
            clientes = json.load(database)
        
        # Verificar se o Cliente já tem divida, se sim, retornar a divida dele atual.
        if int(clientes[matricula]["divida"]) > 0:
            return json.dumps(clientes[matricula])
        
        else:
            # Jogar para ultimo consumo o dado de consumo atual do hidrometro e colocar divida no cliente
            # Pegar dados do banco
            with open("banco/hidrometros.json", 'r' , encoding='utf-8') as database:
                hidrometros = json.load(database)
            
            # atualizar o Ultimo consumo atual e gerar conta
            uc = str(hidrometros[matricula.lower()]["ultimoConsumo"])
            ca = str(hidrometros[matricula.lower()]["consumoAtual"])
            bl = str(hidrometros[matricula.lower()]["bloqueado"])
            va = str(hidrometros[matricula.lower()]["vazando"])
            
            metrosCubicosGastos =  int(ca) - int(uc)
            valorPagar = metrosCubicosGastos * 6      # Cada Metro cubico ta saindo a 6 Reais
            
            hidrometros[matricula.lower()] = {"ultimoConsumo" : ca, "consumoAtual" : ca, "bloqueado" : bl, "vazando" : va}

            #Salvar alterações do hidrometro no banco
            with open("banco/hidrometros.json", 'w' , encoding='utf-8') as database:
                    json.dump(hidrometros, database, indent=4)  
            

            #Atualizar divida no cliente e salvar
            clientes[matricula.lower()] = {"divida" : str(valorPagar)}

            with open("banco/clientes.json", 'w' , encoding='utf-8') as database:
                    json.dump(clientes, database, indent=4)  

            return json.dumps(clientes[matricula])

    
    def PUT_Pagarconta(self, matricula):
        # Desbloquear Hidrometro automaticamente
        self.PUT_DesbloquearHidrometro(matricula)
        
        #Abrir database de clientes
        with open("banco/clientes.json", 'r' , encoding='utf-8') as database:
            clientes = json.load(database)

        # zerar a divida
        clientes[matricula.lower()] = {"divida" : "0"}
        
        #Salvar alterações no banco
        with open("banco/clientes.json", 'w' , encoding='utf-8') as database:
            json.dump(clientes, database, indent=4)  
        
        return json.dumps('{"conta": "paga"}')


    # Metodos Hidrometro


    def PUT_NovoConsumoTotal(self, matricula, novoConsumo, vazando):
        # Mandar os dados de consumo para o banco
        try:
            # Pegar dados do banco
            with open("banco/hidrometros.json", 'r' , encoding='utf-8') as database:
                hidrometros = json.load(database)

            # bloquar hidrometro
            uc = str(hidrometros[matricula.lower()]["ultimoConsumo"])
            bl = str(hidrometros[matricula.lower()]["bloqueado"])
            hidrometros[matricula.lower()] = {"ultimoConsumo" : uc, "consumoAtual" : novoConsumo, "bloqueado" : bl, "vazando" : vazando}
        
            #Salvar alterações no banco
            with open("banco/hidrometros.json", 'w' , encoding='utf-8') as database:
                json.dump(hidrometros, database, indent=4)  

            # Chamar função para gerar boleto do dono do hidrometro.
            self.GET_GerarBoleto(matricula)  
            
            retorno = '{ "bloqueado" : "-" }'.replace("-",bl)
            return json.dumps(retorno)
        except:
            return json.dumps('{ "validar" : "False" }')
    