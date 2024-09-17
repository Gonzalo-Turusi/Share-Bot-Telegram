import requests
from configuration.ConfigEnv import configEnv
from managers.DBManagerSQLLite import DBManagerSQLLite

class SharePercentAlert:
    def __init__(self, bot):
        self.bot = bot
        self.api_key = configEnv.get('ALPHA_VANTAGE')
    
    async def validate(self, chats_id):
        for chat_id in chats_id:
            db_manager = DBManagerSQLLite()
            shares = db_manager.get_shares_by_chat_id(chat_id=chat_id)

            for share in shares:
                share_code = share['share_code']
                share_info = self.get_share_info(share_code)
                if share_info:
                    percent = self._get_percent(share_info)
                    if percent != 'N/A' and (float(percent) > 1.5 or float(percent) < -1.5):
                        message = "¡La acción {} ha variado un {}%!".format(share_code, percent)
                        await self.bot.bot.send_message(chat_id=chat_id, text=message)

    def get_share_info(self, share_code):
        function = 'GLOBAL_QUOTE'
        url = f'https://www.alphavantage.co/query?function={function}&symbol={share_code}&apikey={self.api_key}'
        return requests.get(url).json()

    def _get_percent(self, share_info):
        global_quote = share_info.get('Global Quote', {})
        percent_str = global_quote.get('10. change percent', 'N/A')
        if percent_str != 'N/A':
            percent_str = percent_str.replace('%', '')
            return percent_str
        return 'N/A'