from telegram import Update
from telegram.ext import ContextTypes
from managers.AuthorizationManager import AuthorizationManager
from configuration.ConfigEnv import configEnv

class LoginCommand:
    def __init__(self) -> None:
        self.auth_manager = AuthorizationManager()

    async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_user.id
        user_ad = None
        secret_password = None

        if context.args:
            if len(context.args) == 2:
                user_ad = context.args[0]
                secret_password = context.args[1]
        else:
            await update.message.reply_text("Por favor proporciona tu Usuario de AD.")
            return

        if secret_password is None or secret_password != configEnv.get('VALIDATION_KEY'):
            await update.message.reply_text("No se pudo autenticar correctamente.")
            return

        try:
            self.auth_manager.add_or_update_user(user_ad, chat_id)
            await update.message.reply_text("Se loggueó exitosamente.")
        except Exception as e:
            await update.message.reply_text(f"Ocurrió un error: {str(e)}")