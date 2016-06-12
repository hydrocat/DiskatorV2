from comandoSQL import * 

def SQLcreate(texto):
    texto = " ".join( texto.split() )
    creates = [ x.split() for x in texto.split("create") if len(x) ]
    comandosSQL = [] 

    for create in creates:
        nomeTabela = create[1]
        create = create[2:]
        dados = []
        repBinaria = ">"

        for i in range( 0, len(create), 2 ):
            dado, passo = getDado( create[i:i+3] )
            if len( dado ):
                dados.append(dado)
                create = create[passo:]
                repBinaria += getBin( dado[1:] )
        sql =  comandoSQL(nomeTabela, "create", dados, repBinaria)
        print(sql)
        comandosSQL.append(sql)
         
        
def getBin( tipo ):
    tb = {  "integer":"i", "char":"c",
            "varchar":"c", "boolean":"?",
            "float"  :"f"
         }
    try:
        return tb[tipo[0]]*int(tipo[1])
    except IndexError:
        return tb[tipo[0]]

        
    
def getDado( tripla ):
    try:
        if '.' in tripla[2]:
            tripla[2] = float( tripla[2] )
        else:
            tripla[2] = int( tripla[2] )
        return tripla, 1

    except ValueError:
        return tripla[:2], 0

    except IndexError:
        return tripla[:], -1

def SQLinsert(texto):
    return

def SQLselect(texto):
    return

def parse(arquivo):
    texto = open(arquivo,'r').read()

    t = str.maketrans(";,()", "    ")
    texto = texto.translate(t)

    if   "create" in texto:
        return SQLcreate(texto)
    elif "insert" in texto:
        return SQLinsert(texto)
    elif "delete" in texto:
        return SQLcreate(texto)

if __name__ == "__main__":
    parse( "creates.sql")
