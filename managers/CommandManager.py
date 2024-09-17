from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
from commands.LoginCommand import LoginCommand
from commands.StartCommand import StartCommand
from commands.SuscribeCommand import SuscribeCommand
from commands.UnsuscribeCommand import UnsuscribeCommand
from commands.TestEmailCommand import TestEmailCommand
from commands.AuthorizationMiddleware import AuthorizationMiddleware
from commands.LogoutCommand import LogoutCommand
from commands.InitializeShedulesCommand import InitializeShedulesCommand
from commands.AddShareCommand import AddShareCommand
from commands.RemoveShareCommand import RemoveShareCommand
from commands.FetchBadlarCommand import FetchBadlarCommand
from commands.FetchShareCommand import FetchShareCommand
from commands.DolarMepCommand import DolarMepCommand
from commands.GetMySharesCommand import GetMySharesCommand

class CommandManager:
    def __init__(self):
        self.auth_middleware = AuthorizationMiddleware()
        self.login = LoginCommand()
        self.logout = LogoutCommand()
        self.init_notifications = InitializeShedulesCommand()
        self.start = StartCommand()
        self.suscribe = SuscribeCommand()
        self.unsuscribe = UnsuscribeCommand()
        self.test_email = TestEmailCommand()
        self.add_share = AddShareCommand()
        self.remove_share = RemoveShareCommand()
        self.fetch_share = FetchShareCommand()
        self.fetch_badlar = FetchBadlarCommand()
        self.dolar_mep = DolarMepCommand()
        self.get_my_shares = GetMySharesCommand()

    def add_commands(self, bot):
        # Lista de Comandos
        bot.add_handler(CommandHandler("login", self.login.action))
        bot.add_handler(CommandHandler("logout", self.wrap_with_auth(self.logout.action)))
        bot.add_handler(CommandHandler("initNotifications", self.wrap_with_auth(self.init_notifications.action)))
        bot.add_handler(CommandHandler("start", self.wrap_with_auth(self.start.action)))
        bot.add_handler(CommandHandler("suscribe", self.wrap_with_auth(self.suscribe.action)))
        bot.add_handler(CommandHandler("unsuscribe", self.wrap_with_auth(self.unsuscribe.action)))
        bot.add_handler(CommandHandler("sendEmail", self.wrap_with_auth(self.test_email.action)))
        bot.add_handler(CommandHandler("addShare", self.wrap_with_auth(self.add_share.action)))
        bot.add_handler(CommandHandler("removeShare", self.wrap_with_auth(self.remove_share.action)))
        bot.add_handler(CommandHandler("share", self.wrap_with_auth(self.fetch_share.action)))
        bot.add_handler(CommandHandler("badlar", self.wrap_with_auth(self.fetch_badlar.action)))
        bot.add_handler(CommandHandler("dolarmep", self.wrap_with_auth(self.dolar_mep.action)))
        bot.add_handler(CommandHandler("myShares", self.wrap_with_auth(self.get_my_shares.action)))
        
    def wrap_with_auth(self, handler):
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await self.auth_middleware.check_authorization(update, context, handler)
        return wrapped