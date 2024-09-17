from telegram import Update
from telegram.ext import ContextTypes
from managers.HttpClientManager import HTTPClientManager
from shared.Price_formatter import format_price_arg
from datetime import datetime

class DolarMepCommand:
	def __init__(self):
		url = "https://dolarapi.com/v1/"
		self.http_client_manager = HTTPClientManager(base_url=url)

	async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
		try:
			data = self.http_client_manager.get("dolares/bolsa")

			if data:
				compra = data.get('compra', 'N/A')
				venta = data.get('venta', 'N/A')
				nombre = data.get('nombre', 'N/A')
				moneda = data.get('moneda', 'N/A')
				fecha_actualizacion = data.get('fechaActualizacion', 'N/A')

				formatted_compra = format_price_arg(compra)
				formatted_venta = format_price_arg(venta)

				if fecha_actualizacion != 'N/A':
					fecha_actualizacion_dt = datetime.fromisoformat(fecha_actualizacion.replace("Z", "+00:00"))
					formatted_fecha_actualizacion = fecha_actualizacion_dt.strftime("%d-%m-%Y %H:%M:%S")
				else:
					formatted_fecha_actualizacion = 'N/A'
					
				response_message = (
					f"Nombre: {nombre}\n"
					f"Moneda: {moneda}\n"
					f"Fecha de Actualización: {formatted_fecha_actualizacion}\n"
					f"Compra: {formatted_compra}\n"
					f"Venta: {formatted_venta}"
				)
			else:
				response_message = "No se pudo obtener la información del dolar MEP."

			await update.message.reply_text(response_message)
		except Exception as e:
			await update.message.reply_text(f"Error al obtener la información del dolar MEP: {e}")