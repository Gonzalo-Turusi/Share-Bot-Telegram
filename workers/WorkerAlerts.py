import threading
import time
import logging
from managers.AlertsManager import AlertsManager
import asyncio
from configuration.ConfigEnv import configEnv

class WorkerAlerts:
    def __init__(self):
        self.running = False
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.bot = None
        self.loop = None

    def start(self, bot):
        self.bot = bot
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
                print("Comprobando alertas...")

                if self.bot:
                    alerts_manager = AlertsManager(self.bot)
                    self.loop.run_until_complete(alerts_manager.check_alerts())
                    print("Comprobación alertas finalizada.")
                    
                else:
                    logging.error("El bot no se encuentra instanciado.")

            except Exception as e:
                logging.error("Error en el worker: %s", e)

            self._calculate_time(start_time)

    def _calculate_time(self, start_time):
        elapsed_time = time.time() - start_time
        worker_interval = configEnv.get('WORKER_INTERVAL', default=900)
        if elapsed_time < worker_interval:
            time.sleep(worker_interval - elapsed_time)