import types

def parseCreate(arquivo):
    arquivo = open(arquivo)
    txt = arquivo.read()
    txt.replace('\n',' ')

    #Nome da tabela
    inicio = txt.find("table")
    fim = txt.fim("(")
    nomeTabela = txt[inicio+6 : fim]
    #cria uma classe dinamicamente com o nome da tabela
    tabela = types.new_class(nomeTabela)
    
    #lista de campos
    campos = txt[fim+1:-3] #intervalo dentro dos praentesis
    campos = campos.replace(","," ") #tira as virgulas
    campo = [ x for x in campos.split(" ") if len(x) ]
    
