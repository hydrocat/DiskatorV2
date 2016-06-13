from funcoes import *
import parse
import menu as m
import sys

global arqvs
global valores
arqvs = dict()
valores = dict()

def erro():
    print("A opcao selecionada é invalida.\ndigite um numero de 1 a 5") 

def sair():
    sys.exit(0)

def createArquivo():
    creates = parse("Entre com o nome do arquivo: ") 
    arquivos = [ arquivo(x.nomeTabela) for x in creates ]
    for i in range( len(arquivos)):
        arqvs.update(  { creates[i].nomeTabela :  arquivos[i] })
        valores.update({ creates[i].nomeTabela :  creates[i]  })

    for tabela in arqvs.keys():
        arquivos[tabela].createArquivo( valores[tabela].dados )
        
def inertRegistro():
    inserts = parse("Entre com o nome do arquivo: ")


if __name__ == "__main__":
    string = """0 - Sair
                1 - Criar Arquivo
                2 - Inserir Registro
                3 - Deletar Registro
                4 - Listar Registro"""
    
    funcoes = [ erro, sair, createArquivo, insertRegistro, deleteRegistro, listarRegistro ]
    menu = m.menu(funcoes, string)
