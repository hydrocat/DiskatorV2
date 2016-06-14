class menu:

    """
    Funcoes é uma lista de callbacks 
    sendo que o primeiro é chamado quando a opção escolhida é inválida
    """
    def __init__(self, funcoes, string_menu):
        self.funcoes = funcoes
        self.string_menu = string_menu

    def run(self):
        while True:
#           try:
            op = input( self.string_menu )
            op = int( op )
            func = self.funcoes[op]
            func()

                #self.funcoes[ int( input(self.string_menu) ) + 0 ]()
#           except IndexError:
#               self.funcoes[0]()
#           except TypeError:
#               self.funcoes[0]()

if __name__ == "__main__":
    def DUMMY_criar():
        print("Dummy Criar")

    def DUMMY_inserir():
        print("Dummy inserir")

    def DUMMY_listar():
        print("Dummy listar")

    def DUMMY_excluir():
        print("Dummy Excluir")
         
    def DUMMY_error():
        print("Dummy Erro")
    funcoes = [DUMMY_error, DUMMY_criar, DUMMY_inserir, DUMMY_listar, DUMMY_excluir]
    string_menu = "0 Criar\n1 Inserir\n2 listar\n3 Excluir: "
    menu = menu(funcoes,string_menu)
    menu.run()


