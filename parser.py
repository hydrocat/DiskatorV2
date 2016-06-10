import comandoSQL


def SQLcreate(texto):
    import pdb
    pdb.set_trace()
    nomeTabela = texto[12: texto.find("(")].strip()
    texto = texto[ texto.find("(") : -2]
    campos = [ x.split(" ") for x in texto.split(",") if len(x) ]

    for campo in campos:
        if "char" in campo[2]:
            if "varchar" in campo[2]:
                campo.append( campo[2][campo[2].find("("):campo[2].find(")")]) #append numero
                campo[2] = "varchar"

    return comandoSQL.comandoSQL(nomeTabela,"create",campos)

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