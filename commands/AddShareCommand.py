from alpha_vantage.timeseries import TimeSeries
from telegram import Update
from telegram.ext import ContextTypes
from configuration.ConfigEnv import configEnv
from managers.DBManagerSQLLite import DBManagerSQLLite
from shared.Price_formatter import format_price_usd

class AddShareCommand:
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
				previous_close = format_price_usd(data['08. previous close'].iloc[0])
				
				chat_id = update.message.chat_id
				self.db_manager.add_share(share_code, chat_id)
				
				response_message = (
					f"Información de {share_code}:\n"
					f"Precio Actual: {price}\n"
					f"Cierre Anterior: {previous_close}\n"
					"\nSe agregó exitosamente el símbolo a la lista de seguimiento."
				)
				
			else:
				response_message = f"No se encontró información para {share_code}. Asegúrate de que el símbolo es correcto y vuelve a intentarlo."

			await update.message.reply_text(response_message)
		except Exception as e:
			await update.message.reply_text(f"Error al buscar la información: {str(e)}")