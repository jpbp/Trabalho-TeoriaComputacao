import re
import sys
from copy import copy
from copy import deepcopy #copiar elementos da fita, sem ser o endereco
class Fita:
    def __init__(self):
        self.conteudo = ['B','B']
        self.posicao = 0

    def ler(self):
        return self.conteudo[self.posicao]

    def escrever(self, simbolo):
        self.conteudo[self.posicao] = simbolo
        if(self.posicao == len(self.conteudo)-1):
            self.conteudo.append('B')
    
    def mover(self, direcao):
        
            
        if direcao == 'R':
            self.posicao = self.posicao + 1
        else:
            self.posicao = self.posicao - 1
            if(self.posicao<0):
                raise Exception("Corra, os seguidores de Alanzinho Turing vem ai!!!... by: Terra")
            
    
    def __str__(self):
        string = ""
    
    def imprimir(self):
        print("imprimindo conteudo da fita, posicao cabecote:", end=' ')
        print(self.posicao)
        print(self.conteudo)
    
    def rebobinar(self):
        self.posicao = 0

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
    
    def criaEstados(self, lista):
        if(self.estProx not in lista):
            estado = Estado(self.estProx)
            return estado
        else:
            return None


class Estado:
    def __init__(self, representacao):
        self.representacao = representacao
        self.transicoes = []
        self.contador = 0

    def adicionaTransicao(self, transicao):
        if not isinstance(transicao, Transicao):
            raise Exception("[Estado::adicionaTransicao]: A transicao de um estado necessita ser do tipo Transicao.")
        
        self.transicoes.append(transicao)

    def obterTransicao(self, simboloLido):
        for transicao in self.transicoes:
            if transicao.simLido == simboloLido:
                return transicao
        return None

    def imprime(self):
        print(self.representacao, end=' ')
        print(self.contador)
    
    def getRepresentacao(self):
        return self.representacao
    
    def setRepresentacao(self, nome):
        self.representacao = nome
   

class Maquina:
    def __init__(self):
        self.fitaEntrada = Fita()
        self.fitaTransicao = Fita()
        self.fitaProcesso = Fita()
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
            self.estadoInicial = estado
            self.estadoInicial.contador = 1
            self.estadoAtual = estado
            self.estadoAtual.contador = 1
        
    def processar(self):
        simboloAtual = self.fitaProcesso.ler()
        transicao = self.estadoInicial.obterTransicao(simboloAtual)
        self.fitaTransicao.mover('R')
        self.fitaTransicao.escrever(self.estadoInicial.representacao)
        self.fitaTransicao.mover('R')
        loop = False
        ciclo = []
        contMove = 0
        flagLidoEscrito = False
        while(transicao != None):
            self.fitaProcesso.escrever(transicao.simEscrito)
            self.fitaProcesso.mover(transicao.move)
            flag = False
            if(self.estadoAtual.contador > 1):
                if(transicao.simLido == transicao.simEscrito):
                    flagLidoEscrito = True
                else:
                    flagLidoEscrito = False
                if(transicao.estProx == self.estadoAtual.representacao):
                    if(transicao.simLido == 'B' and transicao.simEscrito == 'B' and transicao.move == 'R'):
                        loop = True
                elif(self.estadoAtual.representacao in ciclo):
                    if(contMove == 0 and flagLidoEscrito == True):
                        print("oi")
                        loop = True
                    else:
                        ciclo = []
                else:
                    if(transicao.move == 'R'):
                        contMove+=1
                    else:
                        contMove-=1
                    ciclo.append(self.estadoAtual.representacao)
            for est in self.estados:
                if(est.representacao == transicao.estProx):
                    self.estadoAtual = est
                    flag = True
            if(loop == True):
                transicao = None
            else:
                self.estadoAtual.contador+=1
                self.fitaTransicao.escrever(self.estadoAtual.representacao)
                self.fitaTransicao.mover('R')
                simboloAtual = self.fitaProcesso.ler()
                transicao = self.estadoAtual.obterTransicao(simboloAtual)
                estParou = self.estadoAtual.representacao
        if(loop == True):
            print("Possivel loop na MTU!")
        else:
            print("Processo finalizado, estado em que parou: ", estParou)
        for i in self.estados:
            i.imprime()

    def imprime(self):
        for est in self.estados:
            est.getRepresentacao()

    def copiar(self):
        self.fitaProcesso = deepcopy(self.fitaEntrada)

    def carregarFitaEntrada(self, entrada):
        self.fitaEntrada = deepcopy(entrada)

    def mostrarConteudoFitas(self):
        print("Fita 1", end=' ')
        self.fitaEntrada.imprimir()
        print("Fita 2", end=' ')
        self.fitaTransicao.imprimir()
        print("Fita 3", end=' ')
        self.fitaProcesso.imprimir()
    
    def verificaEstado(self):
        listEst = []
        parametro = []
        for est in self.estados:
            parametro.append(est.representacao)
        for est in self.estados:
            for tran in est.transicoes:
                novo = tran.criaEstados(parametro)
                if(novo is not None):
                    listEst.append(novo)
        for i in range(len(listEst)):
            if(listEst[i].representacao not in parametro):
                parametro.append(listEst[i].representacao)
                self.estados.append(listEst[i])
                

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
                    simboloLido = 'a'
                elif(cont == 2):
                    simboloLido = 'b'
                else:
                    simboloLido = 'B'
            elif(i == 2):
                #estado prox
                estProx = "q"+str(cont-1)
            elif(i == 3):
                #simbolo escrito
                if(cont == 1):
                    simboloEscrito = 'a'
                elif(cont == 2):
                    simboloEscrito = 'b'
                else:
                    simboloEscrito = 'B'
            else:
                #move
                if(cont == 1):
                    movimento = 'R'
                else:
                    movimento = 'L'
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
    maquinaU = Maquina()
    for i in range(len(listaTrans)):
        name = listaTrans[i].estAtual
        if(name in verifica):
            for est in estados:
                represent = str(est.representacao)
                if(represent == name):
                    est.adicionaTransicao(listaTrans[i])
        else:
            novo_estado = Estado(name)
            novo_estado.adicionaTransicao(listaTrans[i])
            estados.append(novo_estado)
            verifica.append(name)
    c=0
    for est in estados:
        if(c==0):
            maquinaU.adicionaEstado(est,True)
            c=1
        else:
            maquinaU.adicionaEstado(est)
    maquinaU.verificaEstado()
    cont = 0
    x = j+2
    fim = False
    fita = Fita()
    while(fim == False):
        if(mtu[x] == 0 and mtu[x+1] == 0):
            fim = True
        else:
            while(mtu[x] != 0):
                cont+=1
                x+=1
            x+=1
            if(cont == 1):
                fita.escrever('a')
            elif(cont == 2):
                fita.escrever('b')
            elif(cont == 3):
                fita.escrever('B')
            cont = 0
            fita.mover('R')
    fita.rebobinar()
    maquinaU.carregarFitaEntrada(fita)
    maquinaU.copiar()
    return maquinaU
    
        

def main():
    nomearquivo=sys.argv[1]
    arq = open(nomearquivo, 'r')
    texto=str(arq.read())
    texto = texto.replace('\n', '')
    entrada=list(map(int,texto))
    expressao="(000)(((1+)(0)(1+)(0)(1+)(0)(1+)(0)(1+)00))*((1+)(0)(1+)(0)(1+)(0)(1+)(0)(1+))(000)(1+)(01+)*(000)"
    v=re.match(expressao,texto)
    if(v!=None):
        #print(entrada)
        mtu=decoding(entrada)
        mtu.mostrarConteudoFitas()
        mtu.processar()
        mtu.mostrarConteudoFitas()
    else:
        print("entrada nao validada")
    arq.close()

main()