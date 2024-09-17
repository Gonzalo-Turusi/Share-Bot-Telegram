import threading
import time
import logging
from managers.NotificationsManager import NotificationsManager
import asyncio

class WorkerNotifications:
    def __init__(self):
        self.running = False
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.bot = None
        self.loop = None
        self.notifications_manager = None


    def start(self, bot):
        self.bot = bot
        self.notifications_manager = NotificationsManager(self.bot)
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        while self.running:
            start_time = time.time()
            try:
                # Lógica para verificar estados y generar alertas
                print("Comprobando notificaciones...")

                if self.bot:
                    self.loop.run_until_complete(self.notifications_manager.check_notifications())
                    print("Comprobación notificaciones finalizada.")
                else:
                    logging.error("El bot no se encuentra instanciado.")

            except Exception as e:
                logging.error("Error en el worker de notificaciones: %s", e)

            self._calculate_time(start_time)

    def _calculate_time(self, start_time):
        elapsed_time = time.time() - start_time
        worker_interval = 60
        if elapsed_time < worker_interval:
            time.sleep(worker_interval - elapsed_time)