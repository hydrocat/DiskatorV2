import pdb
import copy
import sys
import array
import struct
import parser
#def criaCabecalho():
##esta classe e apenas uma enumeracao
class e:
    nome, tipo, tamanho, valorc = range(4)
    valori = 2

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
                j = str(j)
                if j.isdigit() == True:
                    prevnum = True
                    numcvt += j
                elif prevnum == True:
                    arq.write(struct.pack('>'+'h', int(numcvt))) ##insere o numero inteiro no arquivo
                    numcvt = ''
                    prevnum = False
                    j=" "
                    bytelist = [bytes(x,"utf-8") for x in j]
                    arq.write(struct.pack('>'+'c'*len(j), *bytelist)) #insere todo o metadado bruto com quebra de linhas
                else:
                    j+=" "
                    bytelist = [bytes(x,"utf-8") for x in j]
                    arq.write(struct.pack('>'+'c'*len(j), *bytelist)) #insere todo o metadado bruto com quebra de linhas

            ##se o ultimo parametro era um inteiro entao da um dump no arquivo
            if prevnum == True:
                arq.write(struct.pack('>'+'h', int(numcvt)))
                numcvt = ''
                prevnum = False 
            arq.write(struct.pack('>' + 'c', bytes('\n',"utf-8"))) ##insere uma quebra de linha
        ##encerra o arquivo meta de metadado
        arq.close()
        ##cria o arqivo de dados
        arq = open(self.nome+".data", 'wb')
        ##criando o cabecalho
        arq.write(struct.pack('>'+'hhh', 0,0,2000))
        for i in range(2000-6):
            arq.write(struct.pack('>'+'c',bytes(" ","utf-8")))
        arq.close()
    
    def insertRegistro(self, reg):
        metalinhas = [linhas.rstrip() for linhas in open(self.nome+".met", 'rbU')]
        arq = open(self.nome+".data", 'rb+')
        estrutura = []
        ponteiro = 0
        ##organiza estrutura do metadados
        #pdb.set_trace()
        for linha in metalinhas:
         #   print(metalinhas)
            linha = linha#.decode()
            linha += " \0".encode()
            aux = linha.split()
            estrutura.append(aux)

        ## seta os valores da insercao
        for i in range(len(estrutura)):
            for dad in reg:
                if estrutura[i][e.nome] == dad[0]:
                    if ((estrutura[i][e.tipo] == "integer") or (estrutura[i][e.tipo] == "boolean")):
                        estrutura[i][e.valori] = dad[1]
                    else:
                        #print(dad)
                        estrutura[i][e.valorc] = dad[1]
        #calcula o tamanho da insercao
        tam = len(estrutura) + 2 ##bitmap + ponteiro
        
#       pdb.set_trace()
        for i in estrutura:
            if i[e.tipo] == "integer".encode():
                tam += 4
            elif i[e.tipo] == "boolean".encode():
                tam += 1
            elif i[e.tipo] == "char".encode():
                tam += struct.unpack('>'+'h', i[e.tamanho])[0]
            else:
                tam += len(i[e.valorc]) + 4 
                
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
            ponteiro = cabecalho[2]-tam+1
            novolivre = cabecalho[2]-tam
            bitmap = 0
        #considerando que o dado passado ja esta em binario cria o cabecalho, bitmap e insere
        cablivre = cabecalho[2]
        idx = -1
        for i in estrutura:
            idx += 1
            if len(i) < 4:
                if i[e.valori] == '\0':
                    bitmap += 2 ** (len(estrutura) - (idx+1))
            else:
                if i[e.valorc] == '\0':
                    bitmap += 2 ** (len(estrutura) - (idx+1))
                    
            if i[e.tipo] != "varchar":
                if i[e.tipo] == "char":
     #               if i[e.valorc] == '\0':
      #                  bitmap += 2 ** (len(estrutura) - (idx+1))
                    arq.write(i[e.valorc].encode())
                else:
       #             if i[e.valori] == '\0':
        #                bitmap += 2 ** (len(estrutura) - (idx+1))
                   # print(i[e.valori])
                    if i[e.tipo] == 'integer':
                        arq.write(struct.pack('>'+'i',i[e.valori]))
                    else:
                        if i[e.valori] == 't':
                            i[e.valori] = True
                        else:
                            i[e.valori] = False
                        arq.write(struct.pack('>'+'?',i[e.valori]))
            else:
                posantiga = arq.tell()
                arq.seek(cablivre-len(i[e.valorc])+1,0)
                aponta = arq.tell()
                cablivre -= len(i[e.valorc])
         #           if i[e.valorc] == '\0':
          #              bitmap += 2 ** (len(estrutura) - (idx+1))
                arq.write(i[e.valorc].encode())
                arq.seek(posantiga)
                arq.write(struct.pack('>'+'hh', aponta, len(i[e.valorc])))
        print(str(len(estrutura)) + " valores foram inseridos")             
        arq.write(struct.pack('>'+'H', bitmap))
        arq.seek(4) #atualiza o livres
        arq.write(struct.pack('>'+'h',novolivre))
        arq.seek(6 + (2*cabecalho[0])) #inclui o ponteiro para a criacao
        arq.write(struct.pack('>'+'h', ponteiro))
        arq.seek(0)
        arq.write(struct.pack('>'+'h', cabecalho[0]+1))
        arq.close()  

    def deleteRegistro(self, dado):
        metalinhas = [linhas.rstrip() for linhas in open(self.nome+".met", 'rbU')]
        arq = open(self.nome+".data", 'rb+')
        estrutura = []
        cont = 0
        ##organiza estrutura do metadados
        for linha in metalinhas:
            aux = linha.split()
            if ((aux[1] == "char") or (aux[1] == "varchar")):
                aux[2] = struct.unpack('>'+'h', aux[2])[0]
                aux[0] = [aux[0], aux[1], aux[2]]
            else:
                aux[0] = [aux[0], aux[1]]
            estrutura.append(aux[0])
        
        cabecalhobin = arq.read(6)
        cabecalho = struct.unpack('>'+'hhh', cabecalhobin)
        ##print(cabecalho)
        if cabecalho[0]-cabecalho[1] <= 0:
            print("nao ha registros para ser visualizados")
            return(False)
        else:
            #tira o cabecalho desnecessario
            arq.seek(6)
            ponteiros = []
            for k in range(cabecalho[0]):
                
                ponteirobin = arq.read(2)
                ponteiros.append(struct.unpack('>'+'h', ponteirobin)[0])
            idx = -1
            for p in ponteiros:
                idx += 1
                if p != 0:
                    arq.seek(p)
                    for est in estrutura:
                        if est[e.tipo] == "varchar":
                            getp = (struct.unpack('>'+'hh', arq.read(4)))
                            #print(getp)
                            posantiga = arq.tell()
                            arq.seek(getp[0])
                           # print(arq.read(getp[1]))
                            est[1] = struct.unpack('>'+str(getp[1])+'s', arq.read(getp[1]))[0]
                            arq.seek(posantiga)
                        elif est[e.tipo] == "integer":
                            est[1] = struct.unpack('>'+'i', arq.read(4))[0]
                        elif est[e.tipo] == "char":
                            est[1] = struct.unpack('>'+str(est[2])+'s', arq.read(est[2]))[0]
                        else:
                            est[1] = struct.unpack('>'+'?', arq.read(1))[0]
                        if est[0] == dado[0]:
                            arq.seek(6+(idx*2))
                            cont += 1
                            if dado[1] == '=':
                                if est[1] == dado[2]:
                                    arq.write(struct.pack('>'+'h',0))
                            elif dado[1] == "!=":
                                if est[1] != dado[2]:
                                    arq.write(struct.pack('>'+'h',0))
                            elif dado[1] == '>':
                                if est[1] > dado[2]:
                                    arq.write(struct.pack('>'+'h',0))
                            else:
                                if est[1] < dado[2]: 
                                    arq.write(struct.pack('>'+'h',0))
                                    
                            
                       # print(str(est[0])+": "+str(est[1][0]))
                    arq.seek(0)
                    #print('\r')
        print(str(cont)+ " Registro foram removidos")
        arq.close()                
    
    ##essa funcao precisa fazer a conversao do binario antes de imprimir
    def listarRegistro(self):
        metalinhas = [linhas.rstrip() for linhas in open(self.nome+".met", 'rbU')]
        arq = open(self.nome+".data", 'rb+')
        estrutura = []
        estback = []
    
        ##organiza estrutura do metadados
        for linha in metalinhas:
            aux = linha.split()
            
            if ((aux[1] == "char") or (aux[1] == "varchar")):
                aux[2] = struct.unpack('>'+'h', aux[2])[0]
                aux[0] = [aux[0], aux[1], aux[2]]
            else:
                aux[0] = [aux[0], aux[1]]
            estrutura.append(aux[0])
        bitmap = ["bitmap", 0]
        estrutura.append(bitmap)
         
        cabecalhobin = arq.read(6)
        cabecalho = struct.unpack('>'+'hhh', cabecalhobin)
        ##print(cabecalho)
        estback = copy.copy(estrutura)
        if cabecalho[0]-cabecalho[1] <= 0:
            print("nao ha registros para ser visualizados")
            return(False)
        else:
            #tira o cabecalho desnecessario
            arq.seek(6)
            ponteiros = []
            for k in range(cabecalho[0]):
                
                ponteirobin = arq.read(2)
                ponteiros.append(struct.unpack('>'+'h', ponteirobin)[0])
            for p in ponteiros:
                for linha in metalinhas:
                    aux = linha.split()
                    if ((aux[1] == "char") or (aux[1] == "varchar")):
                        aux[2] = struct.unpack('>'+'h', aux[2])[0]
                        aux[0] = [aux[0], aux[1], aux[2]]
                    else:
                        aux[0] = [aux[0], aux[1]]
                    estrutura.append(aux[0])
                bitmap = ["bitmap", 0]
                estrutura.append(bitmap)
                #print("change")
                printa = []
                #print(p)
                if p != 0:
                    arq.seek(p)
                    for est in estrutura:
                      #  print(est)
                        print(est)
                        print()
                        if est[e.tipo] == "varchar":
                            getp = (struct.unpack('>'+'hh', arq.read(4)))
                            if getp[0] == 0:
                                est[1] = "NULL"
                                continue
                            posantiga = arq.tell()
                            arq.seek(getp[0])
                           # print(arq.read(getp[1]))
                            est[1] = struct.unpack('>'+str(getp[1])+'s', arq.read(getp[1]))[0]
                            arq.seek(posantiga)
                        elif est[e.tipo] == "integer":
                            est[1] = struct.unpack('>'+'i', arq.read(4))[0]
                        elif est[e.tipo] == "char":
                            est[1] = struct.unpack('>'+str(est[2])+'s', arq.read(est[2]))[0]
                        elif est[e.tipo] == "boolean":
                            est[1] = struct.unpack('>'+'?', arq.read(1))[0]
                        elif est[e.tipo] == "bitmap": #bitmap
                            est[1] = bin(struct.unpack('>'+'H', arq.read(2))[0])
                            est[1] = est[1][2:]
                            b = '0'*(len(estrutura)-1-len(b))+b
                            for idx, b in est[1]:
                                if b == '1':
                                    printa[idx][1] = "NULL"
                        
                        printa.append(est)
                    for p in printa:
                        if p[0] != 'bitmap':
                            print(str(p[0])+": "+str(p[1]))
                    
                    arq.seek(0)
                    estrutura = copy.copy(estback)
                    print('\r')
        arq.close()                
        #print(arq.read());
        #arq.close()

if __name__ == "__main__": 
    c = parser.parse("creates.sql")
    i = parser.parse("inserts.sql")
    met = ["nome varchar 100", "idade integer", "sexo char 1"]
    for create in c:
        arquivo(create.nomeTabela).createArquivo(create.dados)
    idx = -1
    for ins in i:
        idx += 1
        if idx != 0:
            arquivo(ins.nomeTabela).insertRegistro(ins.dados)

    arquivo(ins.nomeTabela).listarRegistro()
    reg = [["nome", "daniel"], ["idade",'\x00\x00\x00\x0f' ], ["sexo", 'm']]
    reg1 = [["nome", "danielhue"], ["idade",'\x00\x00\x00\x0f' ], ["sexo", 'j']]

#    arquivo(c.nomeTabela).insertRegistro(c.dado)
 #   arquivo("teste").insertRegistro(reg1)
  #  arquivo("teste").listarRegistro()
