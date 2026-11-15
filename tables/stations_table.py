from dbtable import *

class StationsTable(DbTable):
    """Работа с таблицей."""

    def table_name(self):
        """Возвращает имя таблицы."""
        return self.dbconn.prefix + "stations"


    def columns(self):
        """Вовзращает структуру таблицы."""
        return {
            "id": ["serial", "PRIMARY KEY"],
            "station_name": ["varchar(100)", "NOT NULL"],
            "tariff_zone": ["integer", "NOT NULL", "CHECK (tariff_zone >= 0)"],
            "station_number": ["integer", "NOT NULL", "CHECK (station_number > 0)"]
        }