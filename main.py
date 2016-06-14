from funcoes import *
from parser import *
import menu as m
import sys
import pdb


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
    arqvs = dict()
    valores = dict()
    creates = parse( input("Entre com o nome do arquivo com creates: ")) 
    for c in creates:
        arquivo( c.nomeTabela ).createArquivo( c.dados )
        
def insertRegistro():
    arqvs = dict()
    valores = dict()
    inserts = parse( input("Entre com o nome do arquivo com inserts: ") )
    for i in inserts:
        arquivo(i.nomeTabela).insertRegistro( i.dados )

def deleteRegistro():
    arqvs = dict()
    valores = dict()
    deletes = parse( input("Entre com o nome do arquivo com deletes: ") )
    for d in deletes:
        arquivo( d.nomeTabela ).deleteRegistro( d.dados )
def listarRegistro():
    nomeTabela = input("Entre com o nome da tabela: ")
    arquivo(nomeTabela).listarRegistro()

if __name__ == "__main__":
    string ="""1 - Sair
2 - Criar Arquivo
3 - Inserir Registro
4 - Deletar Registro
5 - Listar Registro
"""
    
    funcoes = [ erro, sair, createArquivo, insertRegistro, deleteRegistro, listarRegistro ]
    menu = m.menu(funcoes, string)
    menu.run()
