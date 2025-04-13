from sshtunnel import SSHTunnelForwarder
import pymysql
from config.config import Config
import socket
class DatabaseConnection:
    def __init__(self):
        self.tunnel = None
        self.connection = None
    def connect(self):
        try:
            self.tunnel = SSHTunnelForwarder(
                (Config.SSH_HOST, Config.SSH_PORT),
                ssh_username=Config.SSH_USERNAME,
                ssh_password=Config.SSH_PASSWORD,
                remote_bind_address=(Config.DB_HOST, Config.DB_PORT),
                local_bind_address=('127.0.0.1', Config.LOCAL_BIND_PORT)
            )
            self.tunnel.start()
            
            self.connection = pymysql.connect(
                host='127.0.0.1',
                port=self.tunnel.local_bind_port,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return self.connection
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            self.disconnect()
            raise

    def disconnect(self):
        if self.connection:
            self.connection.close()
        if self.tunnel and self.tunnel.is_active:
            self.tunnel.stop()
            
    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if query.strip().lower().startswith('select'):
                    return cursor.fetchall()
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Ошибка выполнения запроса: {e}")
            raise