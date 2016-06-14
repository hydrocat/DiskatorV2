from funcoes import *
from parser import *
import menu as m
import sys

global arqvs
global valores
arqvs = dict()
valores = dict()

def erro():
    print(
"""-------------------------------------------
|      A opcao selecionada é invalida     |
|        Digite um numero de 1 a 5        |
| E um parametro correto para a sua opção |
-------------------------------------------"""
) 

def sair():
    sys.exit(0)

def createArquivo():
    creates = parse( input("Entre com o nome do arquivo com creates: ")) 
    arquivos = [ arquivo(x.nomeTabela) for x in creates ]
    for i in range( len(arquivos)):
        arqvs.update(  { creates[i].nomeTabela :  arquivos[i] })
        valores.update({ creates[i].nomeTabela :  creates[i]  })

    for tabela in arqvs.keys():
        arquivos[tabela].createArquivo( valores[tabela].dados )
        
def insertRegistro():
    inserts = parse( input("Entre com o nome do arquivo com inserts: ") )
    for i in inserts:
        arqvs[i.nomeTabela].insertRegistro( i.dados )
        

def deleteRegistro():
    deletes = parse( input("Entre com o nome do arquivo com deletes: ") )
    for d in deletes:
        arqvs[i.nomeTabela].deleteRegistro( i.dados )

def listarRegistro():
    nomeTabela = parse( input("Entre com o nome da tabela: ") )
    arqs[nomeTabela].listarRegistro()

if __name__ == "__main__":
    string ="""0 - Sair
1 - Criar Arquivo
2 - Inserir Registro
3 - Deletar Registro
4 - Listar Registro
"""
    
    funcoes = [ erro, sair, createArquivo, insertRegistro, deleteRegistro, listarRegistro ]
    menu = m.menu(funcoes, string)
    menu.run()
