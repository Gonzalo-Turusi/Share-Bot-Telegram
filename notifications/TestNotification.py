import time
import logging
from managers.EmailManager import EmailManager
from managers.DBManagerSQLLite import DBManagerSQLLite

class TestNotification:
    def __init__(self, bot):
        self.bot = bot
        self.mail_sender = EmailManager()

    async def notify(self, chats_id):
        print("Hice una prueba de la notificación!")
        current_time = time.strftime('%H:%M:%S')
        message = f"{current_time}: Esto es simplemente una notificación de prueba..."
        for chat_id in chats_id:
            try:
                await self.bot.bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                logging.error(f"Error al enviar mensaje a {chat_id}: {e}")
        
        db_sqllite = DBManagerSQLLite()
        recipients = db_sqllite.get_recipients_by_notification("TEST")
        self.mail_sender.send_email_if_needed("Prueba de notificaciones", message, recipients)