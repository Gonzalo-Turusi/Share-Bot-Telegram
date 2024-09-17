# shared/Get_DolarMep.py
from managers.HttpClientManager import HTTPClientManager

class GetDolarMep:
    def __init__(self):
        url = "https://dolarapi.com/v1/"
        self.http_client_manager = HTTPClientManager(base_url=url)

    def get_dolar(self):
        try:
            data = self.http_client_manager.get("dolares/bolsa")

            if data:
                venta = data.get('venta', 'N/A')
                return venta
            else:
                return None
        except Exception as e:
            print(f"Error al obtener la información del dolar MEP: {e}")
            return None