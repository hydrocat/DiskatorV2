class comandoSQL():
    """
    nomeTabela String
    comando CREATE | INSERT | DELETE
    dados lista de pares ("nome do campo","Tipo de dado")
    """

    def __init__(self, nomeTabela, comando, dados):
        self.nomeTabela = nomeTabela
        self.comando = comando
        self.dados = dados
