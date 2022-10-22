class Categoria:
    def __init__(self, 
                 codigo:int=None, 
                 descricao:str=None,
                 valor_diaria:float=None
                 ):
        self.set_codigo(codigo)
        self.set_descricao(descricao)

    def set_codigo(self, codigo:int):
        self.codigo = codigo

    def set_descricao(self, descricao:str):
        self.descricao = descricao

    def set_valor_diaria(self, valor_diaria:float):
        self.valor_diaria = valor_diaria

    def get_codigo(self) -> int:
        return self.codigo

    def get_codigo(self) -> int:
        return self.codigo

    def get_valor_diaria(self) -> float:
        return self.valor_diaria

    def to_string(self) -> str:
        return f"Codigo: {self.get_codigo()} | Descrição: {self.get_descricao() | Valor_diaria: {self.get_valor_diaria()}"