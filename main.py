import menu as m
import funcoes as f
import sys

def erro():
    print("A opcao selecionada é invalida.\ndigite um numero de 1 a 5") 

def sair():
    sys.exit(0)


if __name__ == "__main__":
    string = """0 - Sair
                1 - Criar Arquivo
                2 - Inserir Registro
                3 - Deletar Registro
                4 - Listar Registro"""
    funcoes = [ erro, sair, f.createArquivo, f.insertRegistro, f.deleteRegistro, f.listarRegistro ]
    menu = m.menu(funcoes, string)
