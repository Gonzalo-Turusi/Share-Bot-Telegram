from managers.DBManagerSQLLite import DBManagerSQLLite

class SubscriptionManager:
    def __init__(self):
        pass
    
    def append(self, chat_id: int) -> None:
        db_manager = DBManagerSQLLite()
        db_manager.add_subscription(chat_id)

    def remove(self, chat_id: int) -> None:
        db_manager = DBManagerSQLLite()
        db_manager.remove_subscription(chat_id)

    def get_Users(self) -> list:
        db_manager = DBManagerSQLLite()
        return db_manager.get_subscriptions()