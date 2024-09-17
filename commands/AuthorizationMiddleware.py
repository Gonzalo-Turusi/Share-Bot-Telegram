from telegram import Update
from telegram.ext import ContextTypes
from shared.AuthStatus import AuthStatus
from managers.AuthorizationManager import AuthorizationManager

class AuthorizationMiddleware:
    def __init__(self):
        self.auth_manager = AuthorizationManager()

    async def check_authorization(self, update: Update, context: ContextTypes.DEFAULT_TYPE, next_handler):
        chat_id = update.effective_user.id

        status = self.auth_manager.check_user(chat_id)

        if status == AuthStatus.SUCCESS:
            await next_handler(update, context)
        elif status == AuthStatus.UNAUTHORIZED:
            await update.message.reply_text("No estás autorizado para ejecutar este comando.")
        elif status == AuthStatus.EXPIRED:
            await update.message.reply_text("Tus credenciales expiraron. Por favor loguearse nuevamente.")
