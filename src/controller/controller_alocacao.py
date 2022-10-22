from pydoc import cli
from model.alocacao import Alocacao
from model.clientes import Cliente
from controller.controller_cliente import Controller_Cliente
from model.carro import Carro
from controller.controller_carro import Controller_Carro
from conexion.oracle_queries import OracleQueries
from datetime import date

class Controller_Alocacao:
    def __init__(self):
        self.ctrl_cliente = Controller_Cliente()
        self.ctrl_carro = Controller_Carro()
        
    def inserir_alocacaoself) -> Alocacao:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries(can_write=True)
        
        # Lista os clientes existentes para inserir na alocaaco
        self.listar_clientes(oracle, need_connect=True)
        cpf = str(input("Digite o número do CPF do Cliente: "))
        cliente = self.valida_cliente(oracle, cpf)
        if cliente == None:
            return None

        # Lista os carros existentes para inserir na alocacao
        self.listar_carro(oracle, need_connect=True)
        chassi = str(input("Digite o número do chassi do carro: "))
        carro = self.valida_carro(oracle, chassi)
        if carro == None:
            return None
         
       
        data_atual = date.today()
        
        # Passar a data obrigatória de entrega
        dia = int(input("Dia da entrega do carro: ")
        mes = int(input("Dia da entrega do carro: ")
        ano = int(input("Dia da entrega do carro: ")
        data_entrega = datetime.date(ano, mes, dia)

        
        oracle.connect()

        # Insere e persiste a nova alocação
        oracle.write(f"insert into alocacao values ('{data_entrega}','{data_saida}','{cpf}', '{chassi}')")

        # Recupera os dados da nova alocacao criada transformando-a em um DataFrame

        df_alocacao = oracle.sqlToDataFrame(f"select data_entrega, data_saida, from alocacao where data_entrega = {data_entrega}")
        # Cria um novo objeto Alocacao
        nova_alocacao = Alocacao(df_alocacao.data_entrega.values[0], df_alocacao.data_saida.values[0], cpf, chassi)
        # Exibe os atributos da nova alocacao
        print(nova_alocacao.to_string())
        # Retorna o objeto nova_alocacao para utilização posterior, caso necessário
        return nova_alocacao

    def atualizar_alocacao(self) -> Alocacao:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário a data de entrega cuja alocação será alterada
        dia = int(input("A seguir, passe a data da entrega cuja alocaçaõ será alterada, começando pelo dia : "))        
        mes = int(input("Mês do : "))        
        ano = int(input("Ano : "))   
        data_entrega1 = datetime.date(ano, mes, dia)
     

        # Verifica se a alocação existe na base de dados
        if not self.verifica_existencia_alocacao(oracle, data_entrega):


            # Inserir a nova data de entrega
            dias = int(input("Insira o novo dia para a data de entrega : "))        
            meses = int(input("Insira o mês dia para a data de entrega : "))        
            anos = int(input("Insira o ano dia para a data de entrega : "))   
            data_entrega = datetime.date(anos, meses, dias)


            # Lista os clientes existentes para inserir na alocação
            self.listar_clientes(oracle)
            cpf = str(input("Digite o número do CPF do Cliente: "))
            cliente = self.valida_cliente(oracle, cpf)
            if cliente == None:
                return None

            # Lista os carros existentes para inserir na alocação
            self.listar_carros(oracle)
            chassi = str(input("Digite o número do chassi do carro: "))
            carro = self.valida_carro(oracle, chassi)
            if carro == None:
                return None

            data_atual = date.today()

            # Atualiza a descrição da alocação presente
            oracle.write(f"update alocacao set cpf = '{cliente.get_CPF()}', chassi = '{carro.get_chassi()}', data_saida = to_date('{data_atual}','yyyy-mm-dd', data_entrega = to_date('{data_entrega}','yyyy-mm-dd') where data_entrega = {data_entrega}")
            # Recupera os dados da nova alocacao criado transformando em um DataFrame
            df_alocacao = oracle.sqlToDataFrame(f"select data_entrega, data_saida, from alocacao where data_entrega = {data_entrega}")
            # Cria um novo objeto Alocacao
            alocacao_atualizada = Alocacao(df_alocacao.data_entrega.values[0], df_alocacao.data_saida.values[0], cpf, chassi)
            # Exibe os atributos da nova alocação
            print(alocacao_atualizada.to_string())
            # Retorna o objeto alocacao_atualizada para utilização posterior, caso necessário
            return alocacao_atualizada
        else:
            print(f"A data {data_entrega} não existe.")
            return None

    def excluir_alocacao(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()


        # Solicita ao usuário a data de entrega cuja alocação será alterada
        dia = int(input("Dia da entrega que irá excluir : "))        
        mes = int(input("Mês da entrega que irá excluir : "))        
        ano = int(input("Ano da entrega que irá excluir : "))   
        data_entrega1 = datetime.date(ano, mes, dia)
     

        # Verifica se a alocação existe na base de dados
        if not self.verifica_existencia_alocacao(oracle, data_entrega):               
            # Recupera os dados da nova alocação criada transformando em um DataFrame
            df_alocacao = oracle.sqlToDataFrame(f"select data_entrega, data_saida, chassi, cpf from alocacao where data_entrega1 = {data_entrega1}")
            cliente = self.valida_cliente(oracle, df_alocacao.cpf.values[0])
            carro = self.valida_carro(oracle, df_alocacao.chassi.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir esta alocação? [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, caso a alocacao inteira inteira será excluída!")
                opcao_excluir = input(f"Tem certeza que deseja excluir a alocação da data {data_entrega1} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome a alocação da tabela
                    oracle.write(f"delete from alocacao where data_entrega1 = {data_entrega1}")
                    print("Alocação removida com sucesso!")
                    # Cria um novo objeto alocacao para informar que foi removida
                    alocacao_excluida = Alocacao(df_alocacao.data_entrega.values[0], df_alocacao.data_saida.values[0], cpf, chassi)
                    # Exibe os atributos da alocacao excluída
                    print("Alocação Removida com Sucesso!")
                    print(alocacao_excluida.to_string())
        else:
            print(f"Não existe uma alocação na data {data_entrega1}.")


    def listar_clientes(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select c.cpf
                    , c.rg 
                    , c.data_nascimento
                    , c.cnh
                    , c.nome 
                    , c.endereco 
                from clientes c
                order by c.nome
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def listar_carros(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select car.chassi
                    , car.cor
                    , car.modelo
                    , car.marca
                    , car.placa
                    , car.ano

                from carro car
                order by car.chassi
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))


  def verifica_existencia_alocacao(self, oracle:OracleQueries, data_entrega:date=None) -> bool:
        # Recupera os dados da nova alocação criada transformando em um DataFrame
        df_alocacao = oracle.sqlToDataFrame(f"select data_entrega, data_saida from alocacao where data_entrega = {data_entrega}")
        return df_alocacao.empty


    def valida_cliente(self, oracle:OracleQueries, cpf:str=None) -> Cliente:
        if self.ctrl_cliente.verifica_existencia_cliente(oracle, cpf):
            print(f"O CPF {cpf} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(f"select cpf, rg, data_nascimento, cnh, endereco, nome from clientes where cpf = {cpf}")
            # Cria um novo objeto cliente
            cliente = Cliente(df_cliente.cpf.values[0], df_cliente.rg.values[0], df_cliente.data_nascimento.values[0], df_cliente.cnh.values[0], df_cliente.endereco.values[0], df_cliente.nome.values[0])
            return cliente

    def valida_carro(self, oracle:OracleQueries, chassi:str=None) -> Carro:
        if self.ctrl_carro.verifica_existencia_carro(oracle, chassi):
            print(f"O Chassi {chassi} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo carro criado transformando em um DataFrame
            df_carro = oracle.sqlToDataFrame(f"select chassi, cor, modelo, marca, placa, ano, codigo_categoria from carros where chassi = {chassi}")
            categoria = self.ctrl_alocacao.valida_categoria(oracle, df_carro.codigo_categoria.values[0])
            # Cria um novo objeto Carro
            carro = Carro(df_carro.chassi.values[0], df_carro.cor.values[0], df_carro.modelo.values[0],  df_carro.marca.values[0], df_carro.placa.values[0], df_carro.ano.values[0], categoria)
            return carro