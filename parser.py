import comandoSQL


def SQLcreate(texto):

def SQLinsert(texto):
    return

def SQLselect(texto):
    return

def SQLdelete(texto):
    return

def parse(arquivo):
    texto = open(arquivo,'r').read().replace("\n"," ")
    # pega o comando
    comando = texto[:6]

    if comando == "create":
        return SQLcreate(texto)
    elif comando == "insert":
        return SQLinsert(texto)
    elif comando == "select":
        return  SQLselect(texto)
    elif comando == "delete":
        return SQLdelete(texto)

if __name__ == "__main__":
    print(parse( input() ))
