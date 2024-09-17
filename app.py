import logging
import signal
import sys
from telegram.ext import ApplicationBuilder
from managers.CommandManager import CommandManager
from workers.WorkerAlerts import WorkerAlerts
from workers.WorkerNotifications import WorkerNotifications
from configuration.ConfigEnv import configEnv
from configuration.config import ENVIRONMENT

environment = ENVIRONMENT
configEnv.load_config(environment)

# Configuración del registro
logging.basicConfig(
    filename=configEnv.get('LOG_PATH'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=getattr(logging, configEnv.get('LOG_LEVEL'))
)

TOKEN = configEnv.get('TOKEN')
ALERTS_WORKER = WorkerAlerts()
NOTIFICATION_WORKER = WorkerNotifications()

def main():
    logging.info('La aplicación se inició.')
    try:
        bot = ApplicationBuilder().token(TOKEN).build()
    except Exception as e:
        logging.error("Error al obtener el token: %s. ", e, exc_info=True)
        print("No se pudo iniciar el bot. Verifica el archivo de log para más detalles.")

    try:
        cm = CommandManager()
        cm.add_commands(bot)
    except Exception as e:
        logging.error("Error al agregar los comandos: %s. ", e, exc_info=True)
        print("No se pudo iniciar el bot. Verifica el archivo de log para más detalles.")

    # Inicializar y empezar el worker
    ALERTS_WORKER.start(bot)
    NOTIFICATION_WORKER.start(bot)
    
    # Manejar señales para terminación limpia
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    bot.run_polling()

def signal_handler(sig, frame):
    logging.info('La aplicación se está apagando...')
    
    if ALERTS_WORKER:
        ALERTS_WORKER.stop()

    if NOTIFICATION_WORKER:
        NOTIFICATION_WORKER.stop()
    sys.exit(0)

if __name__ == "__main__":
    main()
