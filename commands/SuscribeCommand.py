from telegram.ext import ContextTypes
from telegram import Update
from managers.SubscriptionManager import SubscriptionManager
import logging

class SuscribeCommand:
    
    def __init__(self):
        self.users = SubscriptionManager()
    
    async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id
        if chat_id in self.users.get_Users():
            await update.message.reply_text(f'Ya te encuentras suscrito a las alertas.')
            return

        self.users.append(chat_id)
        logging.info("El siguiente chat_id se ha SUSCRITO a las alertas: " + str(chat_id))
        await update.message.reply_text(f'Te has suscrito exitosamente a las alertas.')
