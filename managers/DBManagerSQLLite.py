import sqlite3
from datetime import datetime
from configuration.ConfigEnv import configEnv

class DBManagerSQLLite:
    def __init__(self):
        server = configEnv.get('DATABASES', 'BOT_TELEGRAM', 'SERVER')
        db_name = configEnv.get('DATABASES', 'BOT_TELEGRAM', 'SOURCE')
        self.conn = sqlite3.connect(server + db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS AuthorizedUsers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_ad TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            registration_date TEXT NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            date TEXT NOT NULL,
            hour INTEGER NOT NULL,
            minute INTEGER NOT NULL,
            recipients TEXT NOT NULL,
            active BOOLEAN NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS MyShares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            share_code TEXT NOT NULL UNIQUE,
            registration_date TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            FOREIGN KEY (chat_id) REFERENCES AuthorizedUsers(chat_id)
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS SubscriptionAlerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            subscription_date TEXT NOT NULL,
            FOREIGN KEY (chat_id) REFERENCES AuthorizedUsers(chat_id)
        )
        ''')
        self.conn.commit()


    def add_or_update_user(self, user_ad: str, chat_id: int) -> None:
        try:
            cursor = self.conn.cursor()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('SELECT * FROM AuthorizedUsers WHERE user_ad = ?', (user_ad.upper(),))
            user = cursor.fetchone()
            
            if user:
                cursor.execute('''
                UPDATE AuthorizedUsers
                SET chat_id = ?, registration_date = ?
                WHERE user_ad = ?
                ''', (chat_id, current_time, user_ad.upper()))
            else:
                cursor.execute('''
                INSERT INTO AuthorizedUsers (user_ad, chat_id, registration_date)
                VALUES (?, ?, ?)
                ''', (user_ad.upper(), chat_id, current_time))
            
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error en add_or_update_user: {e}")

    def get_user_by_chat_id(self, chat_id: int):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM AuthorizedUsers WHERE chat_id = ?', (chat_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error en get_user_by_chat_id: {e}")
            return None

    def remove_user_by_userAD(self, user_ad: str) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM MyShares WHERE chat_id IN (SELECT chat_id FROM AuthorizedUsers WHERE user_ad = ?)', (user_ad.upper(),))
            cursor.execute('DELETE FROM SubscriptionAlerts WHERE chat_id IN (SELECT chat_id FROM AuthorizedUsers WHERE user_ad = ?)', (user_ad.upper(),))
            cursor.execute('DELETE FROM AuthorizedUsers WHERE user_ad = ?', (user_ad.upper(),))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error en remove_user_by_userAD: {e}")

    def remove_user_by_chat_id(self, chat_id: int) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM MyShares WHERE chat_id = ?', (chat_id,))
            cursor.execute('DELETE FROM SubscriptionAlerts WHERE chat_id = ?', (chat_id,))
            cursor.execute('DELETE FROM AuthorizedUsers WHERE chat_id = ?', (chat_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error en remove_user_by_chat_id: {e}")

    def add_notification(self, name: str, date: str, hour: int, minute: int, recipients: str, active: bool) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT INTO Notifications (name, date, hour, minute, recipients, active)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, date, hour, minute, recipients, active))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error en add_notification: {e}")

    
    def get_notifications(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM Notifications')
            rows = cursor.fetchall()
            notifications = {row[1]: row for row in rows}  # Asumiendo que el nombre de la notificación está en la segunda columna
            return notifications
        except sqlite3.Error as e:
            print(f"Error en get_notifications: {e}")
            return {}

    def notification_exists(self, name: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT COUNT(1) FROM Notifications WHERE name = ?', (name,))
            result = cursor.fetchone()
            return result[0] > 0
        except sqlite3.Error as e:
            print(f"Error en notification_exists: {e}")
            return False

    def get_recipients_by_notification(self, notification_name: str) -> str:
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT recipients FROM Notifications WHERE name = ?', (notification_name,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return ""
        except sqlite3.Error as e:
            print(f"Error en get_recipients_by_notification: {e}")
            return ""
    
    def clear_notifications(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM Notifications')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error en clear_notifications: {e}")

    def add_share(self, share_code: str, chat_id: int) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT OR IGNORE INTO MyShares (share_code, chat_id, registration_date)
            VALUES (?, ?, datetime('now'))
            ''', (share_code, chat_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding share: {e}")

    def delete_share(self, share_code: str) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            DELETE FROM MyShares WHERE share_code = ?
            ''', (share_code,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting share: {e}")

            
    def get_all_shares(self) -> list:
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            SELECT id, share_code, chat_id, registration_date FROM MyShares
            ''')
            rows = cursor.fetchall()
            shares = [{'id': row[0], 'share_code': row[1], 'chat_id': row[2], 'registration_date': row[3]} for row in rows]
            return shares
        except sqlite3.Error as e:
            print(f"Error fetching shares: {e}")
            return []
    
    def get_shares_by_chat_id(self, chat_id: int) -> list:
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            SELECT id, share_code, registration_date FROM MyShares WHERE chat_id = ?
            ''', (chat_id,))
            rows = cursor.fetchall()
            shares = [{'id': row[0], 'share_code': row[1], 'registration_date': row[2]} for row in rows]
            return shares
        except sqlite3.Error as e:
            print(f"Error fetching shares by chat_id: {e}")
            return []

    def add_subscription(self, chat_id: int) -> None:
        try:
            cursor = self.conn.cursor()
            subscription_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
            INSERT INTO SubscriptionAlerts (chat_id, subscription_date)
            VALUES (?, ?)
            ''', (chat_id, subscription_date))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error en add_subscription: {e}")

    def remove_subscription(self, chat_id: int) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            DELETE FROM SubscriptionAlerts WHERE chat_id = ?
            ''', (chat_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error en remove_subscription: {e}")

    def get_subscriptions(self) -> list:
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            SELECT chat_id FROM SubscriptionAlerts
            ''')
            subscriptions = cursor.fetchall()
            return [row[0] for row in subscriptions]
        except sqlite3.Error as e:
            print(f"Error en get_subscriptions: {e}")
            return []