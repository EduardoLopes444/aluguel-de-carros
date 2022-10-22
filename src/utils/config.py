MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Remover Registros
5 - Sair
"""

MENU_RELATORIOS = """Relatórios
1 - Relatório de Carros
2 - Relatório de Alocações
3 - Relatório de Categorias
4 - Relatório de Clientes
0 - Sair
"""

MENU_ENTIDADES = """Entidades
1 - ALOCAÇÕES
2 - CLIENTES
3 - CARROS
4 - CATEGORIAS
"""

# Consulta de contagem de registros por tabela
QUERY_COUNT = 'select count(1) as total_{tabela} from {tabela}'

def clear_console(wait_time:int=3):
    '''
       Esse método limpa a tela após alguns segundos
       wait_time: argumento de entrada que indica o tempo de espera
    '''
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")