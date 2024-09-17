from managers.SubscriptionManager import SubscriptionManager
from alerts.TestAlert import TestAlert
from alerts.SharePercentAlert import SharePercentAlert

class AlertsManager:
    def __init__(self, bot):
        self.bot = bot
        self.users = SubscriptionManager()
        self.test = TestAlert(bot)
        self.share_percent = SharePercentAlert(bot)
    
    async def check_alerts(self):
        users_to_inform = self.users.get_Users()
        
        await self.test.validate(users_to_inform)
        await self.share_percent.validate(users_to_inform)
