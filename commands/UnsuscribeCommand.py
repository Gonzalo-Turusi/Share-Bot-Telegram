from telegram.ext import ContextTypes
from telegram import Update
from managers.SubscriptionManager import SubscriptionManager
import logging

class UnsuscribeCommand:
    
    def __init__(self):
        self.users = SubscriptionManager()
    
    async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.message.chat_id
        if chat_id not in self.users.get_Users():
            await update.message.reply_text(f'No estás suscrito suscrito a las alertas aún.')
            return

        self.users.remove(chat_id)
        logging.info("El siguiente chat_id se ha DESUSCRITO a las alertas: " + str(chat_id))
        await update.message.reply_text(f'Te has desuscrito exitosamente a las alertas.')
