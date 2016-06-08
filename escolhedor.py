class menu:

    """
    Funcoes é uma lista de callbacks 
    sendo que o primeiro é chamdo quando a opção escolhida é inválida
    """
    def __init__(self, funcoes, string_menu):
        self.funcoes = funcoes
        self.string_menu = string_menu

    def run(self):
        while True:
            op = input("1 - Criar Arquivo\n2 - Inserir Registro\n3 - Listar Registros\n4 - Excluir Registros\n5 - Sair\n")
            
            try:
                op = int(op)
                if op == 5:
                    break

                self.funcoes[op-1]()
            except TypeError:
                print("Função inválida")
            except IndexError:
                print("Função inválida")
                


if __name__ == "__main__":
    def DUMMY_criar():
        print("Dummy Criar")

    def DUMMY_inserir():
        print("Dummy inserir")

    def DUMMY_listar():
        print("Dummy listar")

    def DUMMY_excluir():
        print("Dummy Excluir")

    menu = menu(DUMMY_criar, DUMMY_inserir, DUMMY_listar, DUMMY_excluir)
    menu.run()


