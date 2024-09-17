from configuration.ConfigEnv import configEnv
from managers.EmailManager import EmailManager
import logging
import time

class TestAlert:
    def __init__(self, bot):
        self.bot = bot
        self.mail_sender = EmailManager()
    
    async def validate(self, chats_id):
        if not bool(configEnv.get('ALERTS', 'TEST_ACTIVATED')):
            return
        
        print("Hice una prueba de la alerta!")
        current_time = time.strftime('%H:%M:%S')
        message = f"{current_time}: Esto es simplemente una alerta de prueba..."
        for chat_id in chats_id:
            try:
                await self.bot.bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                logging.error(f"Error al enviar mensaje a {chat_id}: {e}")
        self.mail_sender.send_email_if_needed("Prueba de alertas", message, configEnv.get('ALERTS', 'RECIPIENTS'))