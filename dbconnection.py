# Импорт библиотек.
import psycopg2

class DbConnection:
    """Управление базой данных."""

    def __init__(self, config):
        "Подключение к БД."
        self.dbname = config.dbname
        self.user = config.user
        self.password = config.password
        self.host = config.host
        self.prefix = config.dbtableprefix
        self.conn = psycopg2.connect(dbname=self.dbname,
                                     user=self.user, 
                                     password=self.password,
                                     host=self.host)


    def __del__(self):
        """Закрывает соединение с БД при завершении программы."""
        if self.conn:
            self.conn.close()