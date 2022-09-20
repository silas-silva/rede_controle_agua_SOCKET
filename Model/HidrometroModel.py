class Hidrometro:

    def __init__(self):
        self.matricula = 0
        self.bloqueado = False
        self.consumo = 0
        self.vazao = 1
    
    def aumentarVazao(self):
        if(self.bloqueado == False):
            self.vazao += 1
    
    def diminuirVazao(self):
        if(self.bloqueado == False):
            self.vazao -= 1
    
    def bloquear(self):
        self.bloqueado = True
        self.vazao = 0
    
    def desbloquear(self):
        self.bloqueado = False
        self.vazao = 1
