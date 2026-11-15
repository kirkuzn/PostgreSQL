from dbtable import *


class RoutesTable(DbTable):
    """Класс маршрутов поезда."""


    def table_name(self):
        """Возвращает имя таблицы."""
        return self.dbconn.prefix + "route"


    def columns(self):
        """Возвращет структуру таблицы маршрутов."""
        return {
            "id": ["serial", "PRIMARY KEY"],
            "train_number": ["varchar(20)", "NOT NULL", "UNIQUE", "CHECK (train_number ~ '^[0-9]+$')"],
            "start_station_id": ["integer", "NOT NULL", "REFERENCES " + self.dbconn.prefix + "stations(id) ON DELETE CASCADE"],
            "end_station_id": ["integer", "NOT NULL", "REFERENCES " + self.dbconn.prefix + "stations(id) ON DELETE CASCADE"],
            "route_days": ["varchar(20)", "NOT NULL", "CHECK (route_days ~ '^[1-7](,[1-7])*$')"]
        }


    def table_constraints(self):
        """Запрещает создание маршрутов, если начальная/конечная станция совпадают."""
        return ["CHECK (start_station_id <> end_station_id)"]


    def all_by_station(self, station_id):
        """Возвращает список поездов, проходящих через станцию."""
        sql = (
            f"SELECT r.id, r.train_number, "
            f"s1.station_name AS start_name, s2.station_name AS end_name, "
            f"r.route_days "
            f"FROM {self.table_name()} r "
            f"JOIN {self.dbconn.prefix}stations s1 ON r.start_station_id = s1.id "
            f"JOIN {self.dbconn.prefix}stations s2 ON r.end_station_id = s2.id "
            f"WHERE r.start_station_id = %s OR r.end_station_id = %s "
            f"ORDER BY r.id"
        )
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (station_id, station_id))
        return cur.fetchall()