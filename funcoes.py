import sys

#def criaCabecalho(self, dic):
    #dic e o dicionario
 #   self.dic = dic

def criaArquivo(nome):
   arq = open(nome, 'wb')
   arq.write("a")
   arq.close()    

def main(): 
    criaArquivo("uha")
main()
