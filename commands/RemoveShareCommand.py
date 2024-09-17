from telegram import Update
from telegram.ext import ContextTypes
from managers.DBManagerSQLLite import DBManagerSQLLite

class RemoveShareCommand:
	def __init__(self):
		self.db_manager = DBManagerSQLLite()

	async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
		shared_code = ' '.join(context.args)
		if not shared_code:
			await update.message.reply_text("Por favor, proporciona el símbolo del bono o acción que deseas buscar.")
			return

		try:
			self.db_manager.delete_share(shared_code)
			await update.message.reply_text("Se removió exitosamente el símbolo de la lista de seguimiento.")
		except Exception as e:
			await update.message.reply_text(f"Error al intentar remover el símbolo de la lista de seguimiento: {str(e)}")