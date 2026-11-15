from dbconnection import *


class DbTable:
    """Работа с базой данных."""
    dbconn = None


    def __init__(self):
        """Инициализация класса."""
        return


    def table_name(self):
        """Возвращает имя таблицы."""
        return self.dbconn.prefix + "table"


    def columns(self):
        """Возвращает структуру таблицы."""
        return {}


    def column_names_without_id(self):
        """Возвращает список имен колонок."""
        res = list(self.columns().keys())
        if 'id' in res:
            res.remove('id')
        return res


    def primary_key(self):
        """Возвращает название первичного ключа."""
        return ['id']


    def create(self):
        """Создает таблицу в базе данных."""
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in self.columns().items()]
        sql += ", ".join(arr)
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()


    def drop(self):
        """Удаляет таблицу из базы данных."""
        sql = "DROP TABLE IF EXISTS " + self.table_name() + " CASCADE"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()


    def insert_one(self, vals):
        """Добавляет запись в таблицу."""
        placeholders = ", ".join(["%s"] * len(vals))
        sql = f"INSERT INTO {self.table_name()} ({', '.join(self.column_names_without_id())}) VALUES ({placeholders})"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, vals)
        self.dbconn.conn.commit()


    def update_one(self, row_id, vals):
        """Изменяет запись в таблице."""
        set_clause = ", ".join([f"{col} = %s" for col in self.column_names_without_id()])
        sql = f"UPDATE {self.table_name()} SET {set_clause} WHERE id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, vals + [row_id])
        self.dbconn.conn.commit()


    def delete_one(self, row_id):
        """Удаляет запись в таблице."""
        sql = f"DELETE FROM {self.table_name()} WHERE id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (row_id,))
        self.dbconn.conn.commit()


    def count(self):
        """Возвращает записи в таблице."""
        sql = "SELECT COUNT(*) FROM " + self.table_name()
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]


    def page(self, limit, offset):
        """Постраничная запись."""
        sql = f"SELECT * FROM {self.table_name()} ORDER BY id LIMIT %s OFFSET %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (limit, offset))
        return cur.fetchall()


    def all(self):
        """Возвращает все записи."""
        sql = "SELECT * FROM " + self.table_name() + " ORDER BY id"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def find_by_position(self, num):
        """Возвращает запись по номеру."""
        sql = f"SELECT * FROM {self.table_name()} ORDER BY id LIMIT 1 OFFSET %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (num - 1,))
        return cur.fetchone()