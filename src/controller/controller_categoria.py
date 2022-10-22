from model.categoria import Categoria
from conexion.oracle_queries import OracleQueries

class Controller_Categoria:
    def __init__(self):
        pass
        
    def inserir_categoria(self) -> Categoria:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        #Solicita ao usuario a nova descrição da categoria
        descricao_novo = input("Descrição (Novo): ")
        #Solicita ao usuario o novo valor diário
        novo_valor = float(input("Descrição (Novo): "))

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo=output_value, descricao=descricao_novo, valor_diaria=novo_valor )
        # Executa o bloco PL/SQL anônimo para inserção da nova categoria e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :codigo := CATEGORIA_CODIGO_CATEGORIA_SEQ.NEXTVAL;
            insert into categoria values(:codigo, :descricao, :valor_diaria);
        end;
        """, data)
        # Recupera o código da nova categoria
        codigo_categoria = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados da nova categoria criado transformando em um DataFrame
        df_categoria = oracle.sqlToDataFrame(f"select codigo_categoria, descricao, valor_diaria from categorias where codigo_categoria = {codigo_categoria}")
        # Cria um novo objeto Categoria
        nova_categoria = Categoria(df_categoria.codigo_categoria.values[0], df_categoria.descricao.values[0], df_categoria.valor_diaria.values[0])
        # Exibe os atributos da nova categoria
        print(nova_categoria.to_string())
        # Retorna o objeto nova_categoria para utilização posterior, caso necessário
        return nova_categoria

    def atualizar_categoria(self) -> Categoria:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da categoria a ser alterado
        codigo_categoria = int(input("Código da categoria que irá alterar: "))        

        # Verifica se a categoria existe na base de dados
        if not self.verifica_existencia_categoria(oracle, codigo_categoria):

            # Solicita a nova descrição da categoria
            nova_descricao_categoria = input("Descrição (Novo): ")

            # Atualiza a descrição da categoria existente
            oracle.write(f"update categoria set descricao = '{nova_descricao_categoria}' where codigo_categoria = {codigo_categoria}")

            # Recupera os dados da nova categoria criado transformando em um DataFrame
            df_categoria = oracle.sqlToDataFrame(f"select codigo_categoria, descricao, valor_diaria from categoria where codigo_categoria = {codigo_categoria}")

            # Cria um novo objeto Categoria
            categoria_atualizada = Categoria(df_categoria.codigo_categoria.values[0], df_categoria.descricao.values[0], df_categoria.valor_diaria.values[0])

            # Exibe os atributos da nova categoria
            print(categoria_atualizada.to_string())

            # Retorna a categoria_atualizada para utilização posterior, caso necessário
            return categoria_atualizado
        else:
            print(f"O código {codigo_categoria} não existe.")
            return None

    def excluir_categoria(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da categoria a ser alterada
        codigo_categoria = int(input("Código da Categoria que irá excluir: "))        

        # Verifica se a categoria existe na base de dados
        if not self.verifica_existencia_categoria(oracle, codigo_categoria):            
            # Recupera os dados da nova categoria criada transformando em um DataFrame
            df_categoria = oracle.sqlToDataFrame(f"select codigo_categoria, descricao, valor_diaria from categoria where codigo_categoria = {codigo_categoria}")
            # Revome a categoria da tabela
            oracle.write(f"delete from categoria where codigo_categoria = {codigo_categoria}")            
            # Cria um novo objeto Categoria para informar que foi removido
            categoria_excluida = Categoria(df_categoria.codigo_categoria.values[0], df_categoria.descricao.values[0], df_categoria.valor_diaria.values[0] )
            # Exibe os atributos da categoria excluída
            print("Categoria Removida com Sucesso!")
            print(categoria_excluida.to_string())
        else:
            print(f"A categoria {codigo_categoria} não existe.")

    def verifica_existencia_categoria(self, oracle:OracleQueries, codigo:int=None) -> bool:
        # Recupera os dados da nova categoria criado transformando em um DataFrame
        df_categoria = oracle.sqlToDataFrame(f"select codigo_categoria, descricao, valor_diaria from categoria where codigo_categoria = {codigo}")
        return df_categoria.empty