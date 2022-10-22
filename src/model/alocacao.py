from datetime import date
from model.carros import Carro
from model.clientes import Cliente

class Alocacao:
    def __init__(self, 
                 data_entrega:date=None,
                 data_saida:date=None,
                 cliente:Clientes=None,
                 carro:Carro=None
                 ):
        self.set_data_entrega(data_entrega)
        self.set_data_saida(data_saida)
        self.set_cliente(cliente)
        self.set_carro(carro)

    def set_data_entrega(self, data_entrega:date):
        self.data_entrega = data_entrega

    def set_data_saida(self, data_saida:date):
        self.data_saida = data_saida

    
    def set_cliente(self, cliente:Cliente):
        self.cliente = cliente

    def set_carro(self, carro:Carro):
        self.carro = carro

    def get_data_entrega(self) -> date:
        return self.data_entrega

    def get_data_saida(self) -> date:
        return self.data_saida
    
    def get_cliente(self) -> Cliente:
        return self.cliente

    def get_carro(self) -> Carro:
        return self.carro

    def to_string(self):
        return f"Data de entrega: {self.data_entrega()} | Data de saída: {self.data_saida()} | Chassi do carro: {self.get_carro().get_chassi()} | CPF do cliente: {self.get_cliente().get_CPF()}"