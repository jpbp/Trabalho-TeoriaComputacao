
import re
def main():
    arq = open('argumento1.txt', 'r')
    texto=str(arq.read())
    expressao="(000)(((1+)(0)(1+)(0)(1+)(0)(1+)(0)(1+)00))*((1+)(0)(1+)(0)(1+)(0)(1+)(0)(1+))(000)(1+)(01+)*(000)"
    print(re.match(expressao,texto))
    arq.close()
main()