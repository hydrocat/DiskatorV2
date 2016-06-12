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
   texto  = " ".join(texto.split() )
   inserts = [ x.split() for x in texto.split("insert") if len(x)]
   comandosSQL =[]

   for insert in inserts:
       nomeTabela = insert[1]
       insert = insert[2:]
       valores = []
       values = insert.index("values")
       campos = insert[:values]
       dados = insert[values+1:]

       tempDados = []
       tempValor = ""
       temAspas = False
       for dado in dados:
           if dado.count("\"") == 1 and not temAspas:
               tempValor += dado.replace("\"","")
               temAspas = True

           elif dado.count("\"") == 1 and temAspas:
               tempValor += " "+dado.replace("\"","")
               tempDados.append(tempValor)
               temAspas = False
               tempValor = ""

           elif temAspas:
               tempValor += " "+dado

           else:
               tempDados.append(dado.replace("\"",""))

       dados = tempDados
                   
                   
       pares = []
       for i in range( len( dados )):
           pares.append( [ campos[i], dados[i] ] )

       sql =  comandoSQL(nomeTabela, "insert", pares, "")
       comandosSQL.append(sql)
           
   return comandosSQL

def SQLselect(texto):
    return

def parse(arquivo):
    texto = open(arquivo,'r').read()

    t = str.maketrans(";,'()", "     ")
    texto = texto.translate(t)

    if   "create" in texto:
        return SQLcreate(texto)
    elif "insert" in texto:
        return SQLinsert(texto)
    elif "delete" in texto:
        return SQLcreate(texto)

if __name__ == "__main__":
    print (parse( "inserts.sql"))
