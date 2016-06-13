import sys
import array
import struct
#def criaCabecalho():

##esta classe e apenas uma enumeracao
class e:
    nome, tipo, tamanho, valorc = range(4)
    valori = 3

##classe principal do arquivo
class arquivo:
    def __init__(self, nome):
        self.nome = nome
    ##essa funcao cria dois arquivos binarios: "nome.data" e "nome.met" - dados (2kB)  e metadados
    def createArquivo(self, dados):
        ##cria o arquivo de metadados escrita e binario
        arq = open(self.nome+".met", 'wb')
        ##percorre as linhas de parametros 
        for i in dados:
            numcvt = '' ##variavel que armazena numeros inteiros cvt = convert
            prevnum = False ##apenas indica se o numero anterior era um inteiro
            ##percorre cada caractere do parametro para adionar ao arquivo
            for j in i:
                if j.isdigit() == True:
                    prevnum = True
                    numcvt += j
                elif prevnum == True:
                    arq.write(struct.pack('>'+'h', int(numcvt))) ##insere o numero inteiro no arquivo
                    numcvt = ''
                    prevnum = False
                    arq.write(struct.pack('>'+'c', j)) #insere todo o metadado bruto com quebra de linhas
                else:
                    arq.write(struct.pack('>'+'c', j)) #insere todo o metadado bruto com quebra de linhas

            ##se o ultimo parametro era um inteiro entao da um dump no arquivo
            if prevnum == True:
                arq.write(struct.pack('>'+'h', int(numcvt)))
                numcvt = ''
                prevnum = False 
            arq.write(struct.pack('>' + 'c', '\n')) ##insere uma quebra de linha
        ##encerra o arquivo meta de metadado
        arq.close()
        ##cria o arqivo de dados
        arq = open(self.nome+".data", 'wb')
        ##criando o cabecalho
        arq.write(struct.pack('>'+'hhh', 0,0,2000))
        for i in range(2000-6):
            arq.write(struct.pack('>'+'c', ' '))
        arq.close()
    
    def insertRegistro(self, reg):
        metalinhas = [linhas.rstrip() for linhas in open(self.nome+".met", 'rbU')]
        print(metalinhas)
        arq = open(self.nome+".data", 'rb+')
        estrutura = []
        ##organiza estrutura do metadados
        for linha in metalinhas:
            linha += " \0"
            print(linha)
            aux = linha.split()
            estrutura.append(aux)
        ## seta os valores da insercao
        for i in range(len(estrutura)-1):
            for dad in reg:
                if estrutura[i][e.nome] == dad[0]:
                    if ((estrutura[i][e.tipo] == "integer") or (estrutura[i][e.tipo] == "boolean")):
                        estrutura[i][e.valori] = dad[1]
                    else:
                        estrutura[i][e.valorc] = dad[1]
        #calcula o tamanho da insercao
        tam = len(estrutura) ##bitmap
        
        for i in estrutura:
            if i[e.tipo] == "integer":
                tam += 4
            elif i[e.tipo] == "boolean":
                tam += 1
            elif i[e.tipo] == "char":
                tam += i[e.tamanho]
            else:
                tam += len(i[e.valor]) + 4 
                
        #calcula o espaco livre
        free = 0
        cabecalhobin = arq.read(6)
        cabecalho = struct.unpack('>'+'hhh', cabecalhobin)
        free = cabecalho[2] - (6+(cabecalho[0]*2))
    
        #verifica se pode exstir a insercao neste arquivo
        if tam > free:
            print("O arquivo ja esta cheio\nNenhuma insercao foi realizada")
            return (False)
        else:
            arq.seek(cabecalho[2]-tam+1,0) ##aponta para o primeiro livre
            novolivre = cabecalho[2]-tam
            bitmap = 0
        #considerando que o dado passado ja esta em  binario cria o cabecalho, bitmap e insere
        cablivre = cabecalho[2]
        
        for idx, i in estrutura:
            if len(i) < 3:
                if i[e.valori] == '\0':
                    bitmap += 2 ** (len(estrutura) - (idx+1))
            else:
                if i[e.valorc] == '\0':
                    bitmap += 2 ** (len(estrututa) - (idx+1))
                    
            if i[e.tipo] != "varchar":
                if i[e.tipo] == "char":
     #               if i[e.valorc] == '\0':
      #                  bitmap += 2 ** (len(estrutura) - (idx+1))
                    arq.write(i[e.valorc])
                else:
       #             if i[e.valori] == '\0':
        #                bitmap += 2 ** (len(estrutura) - (idx+1))
                    arq.write(i[e.valori])
            else:
                posantiga = arq.tell()
                arq.seek(cablivre-len(i[e.valorc],0))
                cablivre -= len(i[e.valorc])-1
         #           if i[e.valorc] == '\0':
          #              bitmap += 2 ** (len(estrutura) - (idx+1))
                arq.write(i[e.valorc])
                arq.seek(posantiga)
                arq.write(struct.pack('>'+'hh', cablivre+1, len(i[e.valorc])))
                
        arq.write(struct.pack('>'+'H', bitmap))
        arq.seek(4)
        arq.write(struct.pack('>'+'h',novolivre))
        arq.close()  

    def deleteRegistro(self):
        arq = open(self.nome,'wb')
        arq.close() 
    
    ##essa funcao precisa fazer a conversao do binario antes de imprimir
    def listarRegistro(self):
        arq = open(self.nome, 'rb')
        print(arq.read());
        arq.close()


def main(): 
    met = ["nome varchar 100", "idade int", "sexo char 1"]
    arquivo("teste").createArquivo(met)
    reg = [["nome", "daniel"], ["idade", 15], ["sexo", "m"]]
    arquivo("teste").insertRegistro(reg)
main()
