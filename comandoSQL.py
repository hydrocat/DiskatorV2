class comandoSQL():
    """
    nomeTabela String
    comando CREATE | INSERT | DELETE
    dados lista de pares ("nome do campo","Tipo de dado", [valor])

    exemplo CREATE:
        segundo o create a seguir:
        create table alunos(
            ra integer,
            nome varchar(50),
            sexo char(1),
            idade integer,
            altura float
        )

        o objeto cmoandoSQL montado sera equivalente a:
            comandoSQL
                nomeTabela = "alunos"
                comando = "create"
                dados = [
                    [ "ra", "integer" ],
                    [ "nome", "varchar", 50 ],
                    [ "sexo", "char", 1],
                    [ "altura", "float" ]
                ]

    exemplo INSERT:
        segundo o insert a seguir:
            insert into alunos(ra, nome, sexo) values( 
                    1235,
                    "vitorio",
                    'm',
            )

        o objeto cmoandoSQL montado sera equivalente a:
            comandoSQL
                nomeTabela = "alunos"
                comando = "insert"
                dados = [
                    [ "ra", 1235 ],
                    [ "nome", "vitorio"],
                    [ "sexo", "m" ]
                ]


    exemplo DELETE:
        segundo o insert a seguir:
            delete from alunos where nome = "vitorio"

        o objeto cmoandoSQL montado sera equivalente a:
            comandoSQL
                nomeTabela = "alunos"
                comando = "delete"
                dados = [
                    [ "nome", "vitorio" ]
                ]
    """

    def __init__(self, nomeTabela, comando, dados, repBinaria):
        self.nomeTabela = nomeTabela
        self.comando = comando
        self.dados = dados
        self.repBinaria = repBinaria

    def __repr__(self):
        return "{} {} '{}' {}".format(self.nomeTabela, self.comando, self.repBinaria , self.dados )
