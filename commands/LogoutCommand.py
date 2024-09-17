from telegram import Update
from telegram.ext import ContextTypes
from managers.AuthorizationManager import AuthorizationManager

class LogoutCommand:
    def __init__(self) -> None:
        self.auth_manager = AuthorizationManager()

    async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_ad = None
        if context.args:
            user_ad = context.args[0]
        
        chat_id = update.effective_user.id

        try:
            if user_ad is not None:
                self.auth_manager.remove_user_by_userAD(user_ad)
            else:
                self.auth_manager.remove_user_by_chat_id(chat_id)
            await update.message.reply_text("Se deslogueó exitosamente.")
        except Exception as e:
            await update.message.reply_text(f"Ocurrió un error: {str(e)}")