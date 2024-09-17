from managers.SubscriptionManager import SubscriptionManager
from notifications.TestNotification import TestNotification
from notifications.SharesResumeNotification import SharesResumeNotification
from managers.DBManagerSQLLite import DBManagerSQLLite
from datetime import datetime, timedelta

class NotificationsManager:
    def __init__(self, bot):
        self.bot = bot
        self.test = TestNotification(bot)
        self.shares_resume = SharesResumeNotification(bot)
        self.users = SubscriptionManager()
        self.last_execution = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.start_execution = None
        self.notifications = None

    async def check_notifications(self):
        self.start_execution = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        users_to_inform = self.users.get_Users()

        db_manager = DBManagerSQLLite()
        self.notifications = db_manager.get_notifications()

        await self._schedule_notification(self.test.notify, users_to_inform, 'TEST')
        await self._schedule_notification(self.shares_resume.notify, users_to_inform, 'SHARES_RESUME')

        self.last_execution = self.start_execution

    def _is_time_in_range(self, schedule_day, schedule_hour, schedule_minute):
        current_time = datetime.strptime(self.start_execution, "%Y-%m-%d %H:%M:%S")
        if self.last_execution:
            last_exec_time = datetime.strptime(self.last_execution, "%Y-%m-%d %H:%M:%S")
            next_scheduled_time = current_time.replace(hour=schedule_hour, minute=schedule_minute, second=0)
            
            if schedule_day != "Siempre":
                weekday_dict = {'Lun': 0, 'Mar': 1, 'Mie': 2, 'Jue': 3, 'Vie': 4, 'Sab': 5, 'Dom': 6}
                next_scheduled_time = next_scheduled_time + timedelta(days=(weekday_dict[schedule_day] - current_time.weekday()))
            
            if last_exec_time < next_scheduled_time <= current_time:
                return True
            
        return False

    async def _schedule_notification(self, callback, param1, name):
        schedule_str = self._get_schedule_str(name)
        if not schedule_str:
            return
        
        schedule_day, schedule_hour, schedule_minute = schedule_str.split(';')
        schedule_hour, schedule_minute = int(schedule_hour), int(schedule_minute)
        
        if self._is_time_in_range(schedule_day, schedule_hour, schedule_minute):
            await callback(param1)

    def _get_schedule_str(self, name):
        notification = self.notifications.get(name)
        if notification and notification[6]:  # Verificar si la notificación está activa
            return f"{notification[2]};{notification[3]};{notification[4]}"
        return None