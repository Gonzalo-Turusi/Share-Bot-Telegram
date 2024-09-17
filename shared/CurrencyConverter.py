from shared.GetDolarMep import GetDolarMep

class CurrencyConverter:
    def __init__(self, exchange_rate):
        """
        Inicializa el convertidor de divisas con una tasa de cambio.
        
        :param exchange_rate: Tasa de cambio de pesos a dólares.
        """
        self.exchange_rate = exchange_rate

    def pesos_to_dollars(self, amount):
        """
        Convierte una cantidad de pesos a dólares.
        
        :param amount: Cantidad en pesos.
        :return: Cantidad en dólares.
        """
        return amount / self.exchange_rate

    def dollars_to_pesos(self, amount):
        """
        Convierte una cantidad de dólares a pesos.
        
        :param amount: Cantidad en dólares.
        :return: Cantidad en pesos.
        """
        return amount * self.exchange_rate