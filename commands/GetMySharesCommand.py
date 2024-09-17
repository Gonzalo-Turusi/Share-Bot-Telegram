from telegram import Update
from telegram.ext import ContextTypes
from managers.DBManagerSQLLite import DBManagerSQLLite

class GetMySharesCommand:
    def __init__(self):
        self.db_manager = DBManagerSQLLite()

    async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id
        shares = self.db_manager.get_shares_by_chat_id(chat_id=chat_id)

        if not shares:
            await update.message.reply_text("No estás suscrito a ninguna acción.")
        else:
            shares_list = "\n".join([share['share_code'] for share in shares])
            await update.message.reply_text(f"Estás suscrito a las siguientes acciones:\n{shares_list}")