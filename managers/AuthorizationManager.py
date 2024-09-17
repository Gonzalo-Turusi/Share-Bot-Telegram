import os
from datetime import datetime, timedelta
from shared.AuthStatus import AuthStatus
from configuration.ConfigEnv import configEnv
from managers.DBManagerSQLLite import DBManagerSQLLite

class AuthorizationManager:
    def __init__(self) -> None:
        self.db_manager = DBManagerSQLLite()

    def add_or_update_user(self, user_ad: str, chat_id: int) -> None:
        if not self._is_ad_user_admitted(user_ad):
            raise ValueError(f"El usuario '{user_ad}' no está autorizado para usar este aplicativo.")
        
        self.db_manager.add_or_update_user(user_ad, chat_id)

    def check_user(self, chat_id: int) -> AuthStatus:
        user = self.db_manager.get_user_by_chat_id(chat_id)

        if not user:
            return AuthStatus.UNAUTHORIZED

        record_time = datetime.strptime(user[3], "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()

        if (current_time - record_time) > timedelta(days=configEnv.get('CREDENTIAL_VALIDITY_DAYS')):
            self.db_manager.remove_user_by_userAD(user[1])
            return AuthStatus.EXPIRED
        else:
            return AuthStatus.SUCCESS

    def remove_user_by_userAD(self, user_ad: str) -> None:
        self.db_manager.remove_user_by_userAD(user_ad)

    def remove_user_by_chat_id(self, chat_id: int) -> None:
        self.db_manager.remove_user_by_chat_id(chat_id)
        
    def _is_ad_user_admitted(self, user_ad: str) -> bool:
        file_path = configEnv.get('RESOURCES_PATH') + 'ADMITTED_AD_USERS.txt'
        if not os.path.exists(file_path):
            return False

        with open(file_path, 'r') as file:
            for line in file:
                if user_ad.upper() == line.strip().upper():
                    return True
        return False