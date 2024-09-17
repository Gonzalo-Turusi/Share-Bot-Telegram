from telegram import Update
from telegram.ext import ContextTypes
from configuration.ConfigEnv import configEnv
from managers.HttpClientManager import HTTPClientManager

class FetchBadlarCommand:
	def __init__(self):
		api_url = 'https://api.estadisticasbcra.com'
		token = configEnv.get('BCRA')
		self.headers = {
			'Authorization': f'BEARER {token}'
		}
		self.http_client_manager = HTTPClientManager(base_url=api_url)

	async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
		try:
			response = self.http_client_manager.get("tasa_badlar", headers=self.headers)

			data = response

			if data:
				latest_data = data[-1]  # Obtener el dato más reciente
				date = latest_data['d']
				value = latest_data['v']

				response_message = (
					f"Información de la tasa BADLAR:\n"
					f"Fecha: {date}\n"
					f"Valor: {value}"
				)
			else:
				response_message = "No se encontró información para la tasa BADLAR."

			await update.message.reply_text(response_message)
		except Exception as e:
			await update.message.reply_text(f"Error al buscar la información: {str(e)}")