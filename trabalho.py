import re
import sys
from copy import copy
from copy import deepcopy #copiar elementos da fita, sem ser o endereco.
import os
import time

#variáveis para mudar cores no terminal.
RED   = "\033[1;31m"
RESET = "\033[0;0m"

class Fita: #Classe da fita, sendo utilizado lista.
    def __init__(self):
        self.conteudo = ['B','B']
        self.posicao = 0

    def ler(self): #Lê o simbolo da fita de acordo com a transição.
        return self.conteudo[self.posicao]

    def escrever(self, simbolo): #Escreve na fita de acordo com a transição.
        self.conteudo[self.posicao] = simbolo
        if(self.posicao == len(self.conteudo)-1): #Como a fita na MT é infinita, sempre q chega no final adiciona-se mais um 'B'.
            self.conteudo.append('B')
    
    def mover(self, direcao): #Move o cabeçote de leitura, +1 para direita e -1 para esquerda.
        if direcao == 'R':
            self.posicao = self.posicao + 1
        else:
            self.posicao = self.posicao - 1
            if(self.posicao<0): #Caso ocorra quebra da fita.
                raise Exception("Corra, os seguidores de Turing vem ai!!!... by: Terra")
    
    def imprimir(self): #Metodo para imprimir conteudo da fita.
        print("imprimindo conteudo da fita, posicao cabecote:", end=' ')
        print(self.posicao)
        print(self.conteudo)

    def getFita(self): #Metodo para retorna o conteudo da fita.
        return self.conteudo
    
    def rebobinar(self): #Volta para o inicio o cabeçote de leitura, apenas é setado para 0 a posicão do cabeçote na fita (lista).
        self.posicao = 0

class Transicao: #Transições de cada estado, no formato de quintupla.
    def __init__(self, estAtual, simLido, estProx, simEscrito, move):
        self.estAtual = estAtual
        self.simLido = simLido
        self.estProx = estProx
        self.simEscrito = simEscrito
        self.move = move
    
    def imprime(self): #Metodo para impressão, porém retorna os valores direto.
        return (self.estAtual, self.simLido, self.estProx, self.simEscrito, self.move)
    
    def getNome(self): #Retorna o nome do estado atual da transicão.
        return self.estAtual
    
    def criaEstados(self, lista): #Metodo para instanciar estados que não possuam transições.
        if(self.estProx not in lista):
            estado = Estado(self.estProx)
            return estado
        else:
            return None

class Estado: #Classe estado, possui representação (nome do estado), uma lista de transições (quintuplas) e um contador de quantas vezes foi visitado. 
    def __init__(self, representacao):
        self.representacao = representacao
        self.transicoes = []
        self.contador = 0 #Esse contador é utilizado na heuristica da parada.

    def adicionaTransicao(self, transicao): #Adiciona uma transição a lista
        if not isinstance(transicao, Transicao):
            raise Exception("[Estado::adicionaTransicao]: A transicao de um estado necessita ser do tipo Transicao.")
        self.transicoes.append(transicao)

    def obterTransicao(self, simboloLido): #Retorna a transição de acordo com o simbolo lido, caso não exista é retornada nulo.
        for transicao in self.transicoes:
            if transicao.simLido == simboloLido:
                return transicao
        return None

    def imprime(self): #Metodo para impressão do nome do eestado e quantas vezes foi visitado.
        print(self.representacao, end=' ')
        print(self.contador)
    
    def getRepresentacao(self): #Retorna o nome do estado.
        return self.representacao
    
    def setRepresentacao(self, nome): #Muda o nome do estado.
        self.representacao = nome
   
'''Claase da MTU propriamente dita, possuindo três fitas, uma com a entrada recebida,
 uma para colocar os estados visitados e outra para executar a maquina 
 (inicialmente uma cópia da entrada), a heuristica esta implementada nessa classe, 
 ao realizar a execução da maquina. '''
class Maquina:
    def __init__(self):
        self.fitaEntrada = Fita()
        self.fitaTransicao = Fita()
        self.fitaProcesso = Fita()
        self.estadoInicial = None
        self.estadoAtual = None
        self.estados = []

    def adicionaEstado(self, estado, inicial=False): #Adicina um estado a MTU.
        self.estados.append(estado)
        if inicial: #Verifica se é o estado inicial, para instanciar o inicio.
            self.estadoInicial = estado
            self.estadoInicial.contador = 1
            self.estadoAtual = estado
            self.estadoAtual.contador = 1

    '''Metodo que executa a MT, a heuristica implementada identifica um ciclo e faz uma relação
    entre o que esta sendo lido e escrito na fita e o deslocamento do cabeçote de leitura,
    sendo que após identificado o ciclo, caso a fita não seja alterada na segunda iteração
    e o deslocamento tenha sido o mesmo, ou seja, deslocamento 0 a execução é parada e identificado
    um possivel loop. ''' 
    def executar(self): 
        simboloAtual = self.fitaProcesso.ler()
        transicao = self.estadoInicial.obterTransicao(simboloAtual)
        self.fitaTransicao.mover('R')
        self.fitaTransicao.escrever(self.estadoInicial.representacao)
        fita=self.fitaProcesso.getFita()    
        visualizacao(fita,self.fitaProcesso,self.estadoInicial.getRepresentacao(),simboloAtual, transicao.estProx, transicao.simEscrito, transicao.move)
        self.fitaTransicao.mover('R')
        loop = False
        ciclo = [] #Lista para ir adicionando o caminho do ciclo
        contMove = 0
        flagLidoEscrito = False

        '''Enquanto ouver transição e não for identificado um loop
        a execução continua'''
        while(transicao != None):
            self.fitaProcesso.escrever(transicao.simEscrito)
            self.fitaProcesso.mover(transicao.move)
            #Inicio da heuristica
            if(self.estadoAtual.contador > 1):
                if(transicao.simLido == transicao.simEscrito): #Verifica se esta alterando algo na fita.
                    flagLidoEscrito = True
                else:
                    flagLidoEscrito = False
                if(transicao.estProx == self.estadoAtual.representacao):
                    if(transicao.simLido == 'B' and transicao.simEscrito == 'B' and transicao.move == 'R'): #Loop de um estado lendo 'B'.
                        loop = True
                elif(self.estadoAtual.representacao in ciclo): #Verifica se o estado ja esta no ciclo, caso esteja fechou o ciclo.
                    if(contMove == 0 and flagLidoEscrito == True): #Verifica as condições para ver se tem um possivel loop.
                        loop = True
                    else: #Continua execução
                        ciclo = []
                        contMove = 0
                else:
                    if(transicao.move == 'R'):
                        contMove+=1
                    else:
                        contMove-=1
                    ciclo.append(self.estadoAtual.representacao) 
            #Fim da heuristica
            for est in self.estados:
                if(est.representacao == transicao.estProx):
                    self.estadoAtual = est
            if(loop == True):
                transicao = None
            else:
                self.estadoAtual.contador+=1
                self.fitaTransicao.escrever(self.estadoAtual.representacao)
                self.fitaTransicao.mover('R')
                simboloAtual = self.fitaProcesso.ler()
                transicao = self.estadoAtual.obterTransicao(simboloAtual)
                estParou = self.estadoAtual.representacao
                fita=self.fitaProcesso.getFita()
                if(transicao == None):
                    proxEstado = '-'
                    simboloEsc = '-'
                    direcao = '-'
                else:
                    proxEstado = transicao.estProx
                    simboloEsc = transicao.simEscrito
                    direcao = transicao.move
                    '''Função para mostrar execução da MTU'''
                visualizacao(fita,self.fitaProcesso,self.estadoAtual.getRepresentacao(),simboloAtual, proxEstado, simboloEsc, direcao)
        if(loop == True):
            print("Possivel loop na MTU!")
            print("Ciclo: ", end=' ')
            print(ciclo)
        else:
            print("Processo finalizado, estado em que parou: ", estParou)
        
    def copiar(self): #Copia para a fita de processo a entrada.
        self.fitaProcesso = deepcopy(self.fitaEntrada)

    def carregarFitaEntrada(self, entrada): #Passa a entrada para a fita.
        self.fitaEntrada = deepcopy(entrada)

    def mostrarConteudoFitas(self): #Exibe o conteudo das fitas.
        print("Fita 1", end=' ')
        self.fitaEntrada.imprimir()
        print("Fita 2", end=' ')
        self.fitaTransicao.imprimir()
        print("Fita 3", end=' ')
        self.fitaProcesso.imprimir()
    
    def verificaEstado(self): #Verifica se existe algum estado que não tem transição e o cria.
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
                
def visualizacao(conteudo,fita,estAtual,simLido, estProx, simEscrito, direcao): #Metodo para impressão da execução da MTU.
    print("--------------------------Visualização da fita--------------------------")
    print("Estado atual: ",estAtual)
    print("Simbolo lido: ",simLido)
    print("Estado Proximo: ",estProx)
    print("Simbolo escrito: ",simEscrito)
    print("Direçao: ", direcao)
    #print("Posicao da cabeça de leitura: ",posicao)
    for i in range(len(conteudo)):
        
        if(i==fita.posicao):
            print(RED,end="")
            print(conteudo[i],end="")
        else:
            print(RESET,end="")
            print(conteudo[i],end="")
    print(RESET)
    time.sleep(0.5)
    os.system('clear')
   
'''Função que decodifica o arquivo para alto nivel
criando estados e transições, passando-os para a classe da Maquina
e após decodificar a parte das transições e estados, decodifica
a entrada e passa para a fita de entrada da MTU'''
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

    '''Função main, foi utilizado expressão regular para verificar
    se o conteudo do arquivo esta de acordo com as condições 
    para ser uma MTU, é feito o decoding e depois a maquina 
    é executada'''
def main():
    nomearquivo=sys.argv[1]
    arq = open(nomearquivo, 'r')
    texto=str(arq.read())
    texto = texto.replace('\n', '')
    entrada=list(map(int,texto))
    expressao="(000)(((1+)(0)(1+)(0)(1+)(0)(1+)(0)(1+)00))*((1+)(0)(1+)(0)(1+)(0)(1+)(0)(1+))(000)(1+)(01+)*(000)"
    v=re.match(expressao,texto)
    if(v!=None):
        mtu=decoding(entrada)
        mtu.executar()
    else:
        print("entrada nao validada")
    arq.close()

main()