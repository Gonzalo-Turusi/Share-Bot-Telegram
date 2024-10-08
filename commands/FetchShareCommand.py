from alpha_vantage.timeseries import TimeSeries
from telegram import Update
from telegram.ext import ContextTypes
from configuration.ConfigEnv import configEnv
from managers.DBManagerSQLLite import DBManagerSQLLite
from shared.Price_formatter import format_price_usd, format_price_arg
from shared.GetDolarMep import GetDolarMep
from shared.CurrencyConverter import CurrencyConverter

class FetchShareCommand:
	def __init__(self):
		self.api_key = configEnv.get('ALPHA_VANTAGE')
		self.ts = TimeSeries(key=self.api_key, output_format='pandas')
		self.db_manager = DBManagerSQLLite()

	async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
		share_code = ' '.join(context.args)
		if not share_code:
			await update.message.reply_text("Por favor, proporciona el símbolo del bono o acción que deseas buscar.")
			return

		try:
			data, meta_data = self.ts.get_quote_endpoint(symbol=share_code)
			if not data.empty:
				price = format_price_usd(data['05. price'].iloc[0])
				open_price = format_price_usd(data['02. open'].iloc[0])
				high_price = format_price_usd(data['03. high'].iloc[0])
				low_price = format_price_usd(data['04. low'].iloc[0])
				previous_close = format_price_usd(data['08. previous close'].iloc[0])
				
				dolarMep = GetDolarMep().get_dolar()

				if dolarMep == None:
					raise Exception("No se pudo obtener el valor del MEP.")
				
				currency_converter = CurrencyConverter(dolarMep)

				formatted_dolarmep = format_price_arg(str(dolarMep))
				formatted_price_arg = format_price_arg(str(currency_converter.dollars_to_pesos(float(data['05. price'].iloc[0]))))
				formatted_high_arg = format_price_arg(str(currency_converter.dollars_to_pesos(float(data['03. high'].iloc[0]))))
				formatted_low_arg = format_price_arg(str(currency_converter.dollars_to_pesos(float(data['04. low'].iloc[0]))))
				formatted_open_arg = format_price_arg(str(currency_converter.dollars_to_pesos(float(data['02. open'].iloc[0]))))
				formatted_previous_close_arg = format_price_arg(str(currency_converter.dollars_to_pesos(float(data['08. previous close'].iloc[0]))))
				
				response_message = (
					f"Información de {share_code}:\n"
					f"Precio Actual: {price} / {formatted_price_arg}\n"
					f"Apertura: {open_price} / {formatted_open_arg}\n"
					f"Máximo: {high_price} / {formatted_high_arg}\n"
					f"Mínimo: {low_price} / {formatted_low_arg}\n"
					f"Cierre Anterior: {previous_close} / {formatted_previous_close_arg}\n"
                    f"Volumen: {data['06. volume'].iloc[0]}\n"
                    f"Porcentaje de Cambio: {data['10. change percent'].iloc[0]}\n"
					f"\nLa acción cuesta {price}, con un MEP a {formatted_dolarmep}, me daría un precio de {formatted_price_arg}."
				)
			else:
				response_message = f"No se encontró información para {share_code}. Asegúrate de que el símbolo es correcto y vuelve a intentarlo."

			await update.message.reply_text(response_message)
		except Exception as e:
			await update.message.reply_text(f"Error al buscar la información: {str(e)}")