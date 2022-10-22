from pydoc import cli
from model.carros import Carro
from model.categoria import Categoria
from controller.controller_categoria import Controller_Categoria
from conexion.oracle_queries import OracleQueries
from datetime import date

class Controller_Alocacao:
    def __init__(self):
        self.ctrl_categoria = Controller_Categoria()
        
    def inserir_carro(self) -> Carro:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries(can_write=True)
        
        # Lista as categorias existentes para inserir na lista de carros
        self.listar_categorias(oracle, need_connect=True)
        codigo_categoria = int(input("Digite o número de categoria do Carro: "))
        categoria = self.valida_categoria(oracle, codigo_categoria)
        if categoria == None:
            return None


        chassi = str(input("Digite o número do chassi do carro: "))
            
        if not self.verifica_existencia_carro(oracle, chassi):

              cor = str(input("Digite a cor do carro: "))
              modelo = str(input("Digite o nome do modelo do carro: "))
              marca = str(input("Digite o nome da marca do carro: "))
              placa = str(input("Digite o número da placa do carro: "))
              ano = int(input("Digite o ano de lançamento do carro: "))
         
        else:
             print(f"O Carro {chassi} não existe.")
             return None

        
        oracle.connect()

        # Insere e persiste o novo carro
        oracle.write(f"insert into carro values ('{chassi}','{cor}','{modelo}', '{marca}', '{placa}', '{ano}', '{codigo_categoria}')")

        # Recupera os dados do novo carro criado transformando-o em um DataFrame

        df_carro = oracle.sqlToDataFrame(f"select chassi, cor, modelo, marca, placa, ano from carro where chassi = {chassi}")
        # Cria um novo objeto Carro
        novo_carro = Carro(df_carro.chassi.values[0],  df_carro.cor.values[0], df_carro.modelo.values[0], df_carro.marca.values[0], df_carro.placa.values[0], df_carro.ano.values[0], categoria)
        # Exibe os atributos do novo carro
        print(novo_carro.to_string())
        # Retorna o objeto novo_carro para utilização posterior, caso necessário
        return novo_carro

    def atualizar_carro(self) -> Carro:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o número do chassi do carro que terá seus dados alterados
        chassi = str(input("Digite o número do chassi do carro que deseja alterar: "))    


        # Verifica se a alocação existe na base de dados
        if not self.verifica_existencia_carro(oracle, chassi):


            # Lista os categorias existentes para inserir na lista de carros
            self.listar_categorias(oracle)
            codigo_categoria = int(input("Digite o número de categoria do Carro: "))
            categoria = self.valida_categoria(oracle, codigo_categoria)
            if categoria == None:
                return None


            chassi = str(input("Digite o novo o número do chassi: "))    
            cor = str(input("Digite a nova cor do carro: "))
            modelo = str(input("Digite novo o nome do modelo do carro: "))
            marca = str(input("Digite o novo o nome da marca do carro: "))
            placa = str(input("Digite o novo o número da placa do carro: "))
            ano = int(input("Digite o novo o ano de lançamento do carro: "))



            # Atualiza a descrição do carro presente
            oracle.write(f"update carro set chassi = '{chassi}', cor = '{cor}', modelo = '{modelo}', marca = '{marca}', placa = '{placa}', ano = '{ano}', codigo_categoria = '{categoria.get_codigo()}' where data_entrega = {data_entrega}")
            # Recupera os dados do novo carro criado transformando em um DataFrame
            df_carro = oracle.sqlToDataFrame(f"select chassi, cor, modelo, marca, placa, ano from carro where chassi = {chassi}")
            # Cria um novo objeto Carro
            carro_atualizado = Carro(df_carro.chassi.values[0],  df_carro.cor.values[0], df_carro.modelo.values[0], df_carro.marca.values[0], df_carro.placa.values[0], df_carro.ano.values[0], categoria)
            # Exibe os atributos do novo carro
            print(carro_atualizado.to_string())
            # Retorna o objeto carro_atualizado para utilização posterior, caso necessário
            return carro_atualizado
        else:
            print(f"O Carro do chassi de número {chassi} não existe.")
            return None

    def excluir_carro(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()


        #Solicita ao usuário o número do chassi do carro que terá seus dados excluídos
        chassi = str(input("Digite o número do chassi do carro que deseja alterar: "))    
     

        # Verifica se o carro existe na base de dados
        if not self.verifica_existencia_carro(oracle, chassi):        
            # Recupera os dados da nova alocação criada transformando em um DataFrame
            df_carro = oracle.sqlToDataFrame(f"select chassi, cor, modelo, marca, placa, ano, codigo_categoria from carro where chassi = {chassi}")
            categoria = self.valida_categoria(oracle, df_carro.codigo_categoria.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir este carro? [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, os dados inteiros do carro serão excluídos!")
                opcao_excluir = input(f"Tem certeza que deseja excluir os dados do carro de chassi {chassi} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Remove o carro da tabela
                    oracle.write(f"delete from carro where chassi = {chassi}")
                    print("Carro removida com sucesso!")
                    # Cria um novo objeto carro para informar que foi removido
                    carro_excluido = Carro(df_carro.chassi.values[0],  df_carro.cor.values[0], df_carro.modelo.values[0], df_carro.marca.values[0], df_carro.placa.values[0], df_carro.ano.values[0], categoria)
                    # Exibe os atributos do carro excluído
                    print("Carro Removido com Sucesso!")
                    print(carro_excluido.to_string())
        else:
            print(f"Não existe uma alocação na data {data_entrega1}.")


    def listar_categoria(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select cat.codigo_categoria
                    , cat.rg 
                    , cat.data_nascimento
                    , cat.valor_diaria
                from categoria cat
                order by cat.codigo_categoria
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


  def verifica_existencia_carro(self, oracle:OracleQueries, chassi:str=None) -> bool:
        # Recupera os dados da nova alocação criada transformando em um DataFrame
        df_carro = oracle.sqlToDataFrame(f"select chassi, cor, modelo, marca, placa, ano from carro where chassi = {chassi}")
        return df_carro.empty


    def valida_categoria(self, oracle:OracleQueries, codigo_categoria:str=None) -> Categoria:
        if self.ctrl_categoria.verifica_existencia_categoria(oracle, codigo_categoria):
            print(f"A categoria {codigo_categoria} informada não existe.")
            return None
        else:
            oracle.connect()
            # Recupera os dados da nova categoria criada transformanda em um DataFrame
            df_categoria = oracle.sqlToDataFrame(f"select codigo, descricao, valor_diaria from categoria where codigo = {codigo_categoria}")
            # Cria um novo objeto categoria
            categoria = Categoria(df_categoria.codigo.values[0], df_categoria.descricao.values[0], df_categoria.valor_diaria.values[0])
            return categoria

    def valida_carro(self, oracle:OracleQueries, chassi:str=None) -> Carro:
        if self.ctrl_carro.verifica_existencia_carro(oracle, chassi):
            print(f"O Chassi {chassi} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo carro criado transformando em um DataFrame
            df_carro = oracle.sqlToDataFrame(f"select chassi, cor, modelo, marca, placa, ano, codigo_categoria from carros where chassi = {chassi}")
            categoria = self.ctrl_carro.valida_categoria(oracle, df_carro.codigo_categoria.values[0])
            # Cria um novo objeto Carro
            carro = Carro(df_carro.chassi.values[0], df_carro.cor.values[0], df_carro.modelo.values[0],  df_carro.marca.values[0], df_carro.placa.values[0], df_carro.ano.values[0], categoria)
            return carro