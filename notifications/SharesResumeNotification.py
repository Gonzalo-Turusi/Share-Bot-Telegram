import requests
from configuration.ConfigEnv import configEnv
from managers.DBManagerSQLLite import DBManagerSQLLite
from shared.Price_formatter import format_price_usd, format_price_arg
from shared.GetDolarMep import GetDolarMep
from shared.CurrencyConverter import CurrencyConverter

class SharesResumeNotification:
    def __init__(self, bot):
        self.bot = bot
        self.api_key = configEnv.get('ALPHA_VANTAGE')

    async def notify(self, chats_id):
        for chat_id in chats_id:
            db_manager = DBManagerSQLLite()
            shares = db_manager.get_shares_by_chat_id(chat_id=chat_id)
            if not shares:
                await self.bot.bot.send_message(chat_id=chat_id, text="No estás suscripto a ninguna acción.")
                return
            else:
                await self.bot.bot.send_message(chat_id=chat_id, text="Resumen Diario:")

            for share in shares:
                share_code = share['share_code']
                share_info = self.get_share_info(share_code)
                if share_info:
                    message = self.format_share_info(share_info)
                    await self.bot.bot.send_message(chat_id=chat_id, text=message)

    def get_share_info(self, share_code):
        function = 'GLOBAL_QUOTE'
        url = f'https://www.alphavantage.co/query?function={function}&symbol={share_code}&apikey={self.api_key}'
        return requests.get(url).json()

    def format_share_info(self, share_info):
        global_quote = share_info.get('Global Quote', {})
        
        formatted_price = format_price_usd(global_quote.get('05. price', 'N/A'))
        formatted_open = format_price_usd(global_quote.get('02. open', 'N/A'))
        formatted_high = format_price_usd(global_quote.get('03. high', 'N/A'))
        formatted_low = format_price_usd(global_quote.get('04. low', 'N/A'))
        formatted_previous_close = format_price_usd(global_quote.get('08. previous close', 'N/A'))

        dolarMep = GetDolarMep().get_dolar()
        if dolarMep == None:
            raise Exception("No se pudo obtener el valor del MEP.")
        
        currency_converter = CurrencyConverter(dolarMep)

        formatted_dolarmep = format_price_arg(str(dolarMep))
        formatted_price_arg = format_price_arg(str(currency_converter.dollars_to_pesos(float(global_quote.get('05. price', 'N/A')))))
        formatted_high_arg = format_price_arg(str(currency_converter.dollars_to_pesos(float(global_quote.get('03. high', 'N/A')))))
        formatted_low_arg = format_price_arg(str(currency_converter.dollars_to_pesos(float(global_quote.get('04. low', 'N/A')))))
        formatted_open_arg = format_price_arg(str(currency_converter.dollars_to_pesos(float(global_quote.get('02. open', 'N/A')))))
        formatted_previous_close_arg = format_price_arg(str(currency_converter.dollars_to_pesos(float(global_quote.get('08. previous close', 'N/A')))))
        
        return (
            f"Información de la Acción: {global_quote.get('01. symbol', 'N/A')}\n"
            f"Apertura: {formatted_open} / {formatted_open_arg}\n"
            f"Máximo: {formatted_high} / {formatted_high_arg}\n"
            f"Mínimo: {formatted_low} / {formatted_low_arg}\n"
            f"Precio: {formatted_price} / {formatted_price_arg}\n"
            f"Volumen: {global_quote.get('06. volume', 'N/A')}\n"
            f"Último Día de Negociación: {global_quote.get('07. latest trading day', 'N/A')}\n"
            f"Cierre Anterior: {formatted_previous_close} / {formatted_previous_close_arg}\n"
            f"Cambio: {global_quote.get('09. change', 'N/A')}\n"
            f"Porcentaje de Cambio: {global_quote.get('10. change percent', 'N/A')}\n"
            f"\nLa acción cuesta {formatted_price}, con un MEP a {formatted_dolarmep}, me daría un precio de {formatted_price_arg}."
        )