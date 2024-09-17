from telegram.ext import ContextTypes
from telegram import Update
from managers.DBManagerSQLLite import DBManagerSQLLite
import configuration.config as config

class InitializeShedulesCommand:
    def __init__(self):
        self.notifications = None

    async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Estoy consultando la base de datos...')
        db = DBManagerSQLLite()

        # Definir las notificaciones según el ambiente
        if config.ENVIRONMENT == "DESA":
            self._notifications_desa()
        elif config.ENVIRONMENT == "TEST":
            self._notifications_test()
        elif config.ENVIRONMENT == "PROD":
            self._notifications_prod()
        else:
            await update.message.reply_text(f'Ambiente desconocido: {config.ENVIRONMENT}')
            return

        try:
            db.clear_notifications()
            for name, day, hour, minute, emails, active in self.notifications:
                if not db.notification_exists(name):
                    db.add_notification(name, day, hour, minute, emails, active)
            await update.message.reply_text(f'Se dieron de alta las notificaciones exitosamente!')
        except Exception as e:
            await update.message.reply_text(f'No se pudo insertar las notificaciones correctamente: {str(e)}')

    def _notifications_desa(self):
        self.notifications = [
                ("TEST", "Siempre", 18, 37, "gonsalot@gmail.com", True),
                ("SHARES_RESUME", "Siempre", 10, 45, "gonsalot@gmail.com", True),
            ]
        
    def _notifications_test(self):
        self.notifications = [
                ("TEST", "Jue", 16, 5, "gonsalot@gmail.com", False),
                ("TEST2", "Mie", 1, 39, "gonsalot@gmail.com", False),
            ]
        
    def _notifications_prod(self):
        self.notifications = [
                ("TEST", "Jue", 16, 5, "gonsalot@gmail.com", False),
                ("TEST2", "Mie", 1, 39, "gonsalot@gmail.com", False),
            ]

