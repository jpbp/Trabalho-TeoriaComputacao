import re
from enum import Enum

class Simbolo(Enum):
    a = 1
    b = 2
    B = 3

class Direcao(Enum):
    
    right = 1
    left = 2
    

class Fita:
    def __init__(self):
        self.conteudo = [Simbolo.B,Simbolo.B]
        self.posicao = 0

    def ler(self):
        return self.conteudo[self.posicao]

    def escrever(self, simbolo):
        self.conteudo[self.posicao] = simbolo
    
    def mover(self, direcao):
        if direcao == Direcao.right:
            self.posicao = self.posicao + 1
        else:
            self.posicao = self.posicao - 1
    
    def __str__(self):
        string = ""

        
            


class Transicao:
    def __init__(self, estAtual, simLido, estProx, simEscrito, move):
        self.estAtual = estAtual
        self.simLido = simLido
        self.estProx = estProx
        self.simEscrito = simEscrito
        self.move = move
    
    def imprime(self):
        return (self.estAtual, self.simLido, self.estProx, self.simEscrito, self.move)
    
    def getNome(self):
        return self.estAtual


class Estado:
    def __init__(self, representacao):
        self.representacao = representacao
        self.transicoes = []

    def adicionaTransicao(self, transicao):
        if not isinstance(transicao, Transicao):
            raise Exception("[Estado::adicionaTransicao]: A transicao de um estado necessita ser do tipo Transicao.")
        
        self.transicoes.append(transicao)

    def obterTransicao(self, simboloLido):
        for transicao in self.transicoes:
            if transicao.leitura == simboloLido:
                return True

        return False
    def imprime(self):
        for i in self.transicoes:
            print(i.estAtual, i.simLido, i.estProx, i.simEscrito, i.move)
    
    def getRepresentacao(self):
        return self.representacao
   

class Maquina:
    def __init__(self):
        self.fita = Fita()
        self.estadoInicial = None
        self.estadoAtual = None

        self.estados = []

    """
        Adiciona um novo estado na representacao da maquina de Turing.

        Parametros: 
            1) estado: simbologia de estado, instancia da classe Estado
            2) inicial: flag que indica se estado e ou nao inicial
    """
    def adicionaEstado(self, estado, inicial=False):
        if not isinstance(estado, Estado):
            raise Exception("[Maquina::adicionaEstado]: Os estados de uma maquina de turing precisam ser instancias de Estado.")

        self.estados.append(estado)
        
        if inicial:
            self.estadoAtual = estado
        
    def atuar(self):
        simboloAtual = self.fita.ler()
        transicao = self.estadoAtual.obterTransicao(simboloAtual)

        if (transicao is not None):
            self.fita.escrever(transicao.escrita)
            self.fita.mover(transicao.direcao)
    def imprime(self):
        for est in self.estados:
            est.imprime()
            

def decoding(mtu):
    fim=False
    j=3
    cont = 0
    listaTrans = []
    while(fim == False):
        for i in range(5):
            while(mtu[j] != 0):
                cont+=1
                j+=1
            if(i == 0):
                #estado atual
                estAtual = "q"+str(cont-1)
            elif(i == 1):
                #simbolo lido
                if(cont == 1):
                    simboloLido = Simbolo.a
                elif(cont == 2):
                    simboloLido = Simbolo.b
                else:
                    simboloLido = Simbolo.B
            elif(i == 2):
                #estado prox
                estProx = "q"+str(cont-1)
            elif(i == 3):
                #simbolo escrito
                if(cont == 1):
                    simboloEscrito = Simbolo.a
                elif(cont == 2):
                    simboloEscrito = Simbolo.b
                else:
                    simboloEscrito = Simbolo.B
            else:
                #move
                if(cont == 1):
                    movimento = Direcao.right
                else:
                    movimento = Direcao.left
            cont = 0
            j+=1
        
        if(mtu[j] == 0 and mtu[j+1] == 1):
            j+= 1
        if(mtu[j] == 0 and mtu[j+1] == 0):
            fim = True
        transicao = Transicao(estAtual, simboloLido, estProx, simboloEscrito, movimento)
        listaTrans.append(transicao)
    verifica = []
    estados = []
    for i in range(len(listaTrans)):
        if(listaTrans[i].getNome() in verifica):
            for est in estados:
                if(est.getRepresentacao() == listaTrans[i].getNome()):
                    est.adicionaTransicao(listaTrans[i])
        else:
            novo_estado = Estado(listaTrans[i].getNome())
            novo_estado.adicionaTransicao(listaTrans[i])
            estados.append(novo_estado)
            verifica.append(listaTrans[i].getNome())
    maquinaU = Maquina()
    c=0
    for est in estados:
        if(c==0):
            maquinaU.adicionaEstado(est,True)
        maquinaU.adicionaEstado(est)
        c+=1
    
    return maquinaU
    
        





def main():
    #nomearquivo=input()
    arq = open('argumento1.txt', 'r')
    texto=str(arq.read())
    entrada=list(map(int,texto))
    expressao="(000)(((1+)(0)(1+)(0)(1+)(0)(1+)(0)(1+)00))*((1+)(0)(1+)(0)(1+)(0)(1+)(0)(1+))(000)(1+)(01+)*(000)"
    v=re.match(expressao,texto)
    if(v!=None):
        #print(entrada)
        mtu=decoding(entrada)
        mtu.imprime()

        fita=Fita()
        print(fita.conteudo,fita.posicao)
        fita.escrever(Simbolo.a)
        fita.mover(Direcao.right)
        print(fita.conteudo,fita.posicao)
        fita.mover(Direcao.right)
        print(fita.conteudo,fita.posicao)
        fita.mover(Direcao.right)
        print(fita.conteudo,fita.posicao)
        
    else:
        print("entrada nao validada")
    arq.close()

main()