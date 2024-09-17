from telegram.ext import ContextTypes
from telegram import Update
import socket

class StartCommand:
    
    def __init__(self):
        pass
    
    async def action(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        comandos = [
            "/start - Inicia el bot",
            "/login - Iniciar sesión",
            "/suscribe - Suscribirse a alertas",
            "/unsuscribe - Desuscribirse de alertas",
            "/addShare - Añadir una acción",
            "/removeShare - Eliminar una acción",
            "/share - Obtener información de una acción",
            "/myShares - Obtener mis acciones",
            "/dolarMep - Información del dólar MEP",
            "/badlar - Información de BADLAR",
            "/logout - Cerrar sesión",
        ]
        
        comandos_formateados = "\n".join(comandos)
        
        await update.message.reply_text(
            f'¡Hola {update.effective_user.first_name}! Estos son los comandos disponibles:\n{comandos_formateados}')
        await update.message.reply_text(
            f'La aplicación está corriendo en la máquina: {socket.gethostname()}')
