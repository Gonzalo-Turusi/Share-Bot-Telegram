from telegram.ext import ContextTypes
from telegram import Update
from managers.EmailManager import EmailManager
from configuration.ConfigEnv import configEnv

class TestEmailCommand:

    def __init__(self):
        self.mail_sender = EmailManager()

    async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Enviando email de prueba...")
        
        username = update.effective_user.first_name

        recipients = configEnv.get('NOTIFICATIONS', 'ALERTS_RECIPIENTS')

        result = self.mail_sender.send_email_if_needed("Prueba de Envio de mail Bot Telegram", "Esto es una prueba del bot de telegram hecha por " + username, recipients)
        
        if result:
            await update.message.reply_text("El mail de prueba se envió correctamente!")
        else:
            await update.message.reply_text("Hubo un error al enviar el mail de prueba.")