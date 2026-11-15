# Выполнил: Кузнецов Кирилл. Группа М26-555.
# Вариант 6. Таблицы: поезда и станции без связей с другими таблицами.
# Интерфейс только для станции начала и конца.
# Сделано: добавление, редактирование, удаление, вывод, защита от SQL-injection уязвимостей.

import sys
sys.path.append('tables')
from project_config import *
from dbconnection import *
from stations_table import *
from routes_table import *


class Main:
    """Класс взаимодействия с пользователем."""
    config = ProjectConfig()
    connection = DbConnection(config)


    def __init__(self):
        """Подключение к базе данных."""
        DbTable.dbconn = self.connection
        self.page_size = 5


    def get_safe_int(self, prompt, min_val=1, max_val=None, allow_cancel=False):
        """Запрашивает число у пользователя."""
        while True:
            try:
                val_str = input(prompt).strip()
                if allow_cancel and val_str == "0":
                    return 0
                val = int(val_str)
                if val < min_val:
                    print(f"Ошибка: число должно быть не меньше {min_val}.")
                    continue
                if max_val is not None and val > max_val:
                    print(f"Ошибка: число должно быть не больше {max_val}.")
                    continue
                return val
            except ValueError:
                print("Ошибка: пожалуйста, введите целое число (цифрами).")


    def db_init(self):
        """Инициализация базы данных."""
        st = StationsTable()
        rt = RoutesTable()
        rt.drop()
        st.drop()
        st.create()
        rt.create()
        st.insert_one(["Иглино", 6, 1])
        st.insert_one(["Тауш", 5, 2])
        st.insert_one(["Индустриальный парк", 4, 3])
        st.insert_one(["Шакша", 3, 4])
        st.insert_one(["Спортивная", 2, 5])
        st.insert_one(["Москворечье", 1, 6])
        st.insert_one(["Черниковка", 1, 7])
        st.insert_one(["Парковая", 1, 8])
        st.insert_one(["Воронки", 1, 9])
        st.insert_one(["Уфа", 1, 10])
        rt.insert_one(["1000", 1, 10, "1,2,3,4,5,6,7"])
        rt.insert_one(["1001", 1, 7, "1,2,3,4,5"])
        rt.insert_one(["1002", 1, 8, "1,2,3,4,5,6,7"])
        rt.insert_one(["1003", 1, 9, "1,2,3,4,5"])
        rt.insert_one(["1004", 2, 6, "1,2,3,4,5,6,7"])
        rt.insert_one(["1005", 2, 4, "1,3,5,7"])
        rt.insert_one(["1006", 2, 3, "2,3,4,5"])
        rt.insert_one(["1007", 3, 10, "1,2,3,4,5,6"])
        rt.insert_one(["1008", 3, 10, "2,4,6"])
        rt.insert_one(["1009", 3, 9, "1,2,3,4,5"])
        rt.insert_one(["2000", 4, 10, "1,2,3,4,5"])
        rt.insert_one(["2001", 4, 8, "1,2,3,4,5,7"])
        rt.insert_one(["2002", 4, 7, "1,2,3,4,7"])
        rt.insert_one(["2003", 4, 10, "1,2,3,4,5"])


    def main_cycle(self):
        """Основной цикл программы."""
        while True:
            print("-"*34)
            print("СИСТЕМА УПРАВЛЕНИЯ РАСПИСАНИЕМ")
            print("-"*34)
            print("1. Управление станциями")
            print("2. Управление поездами, маршрутами")
            print("3. Сброс и инициализация БД")
            print("9. Выход")
            print("-"*34)
            choice = input("=> ").strip()
            if choice == "1":
                self.menu_stations()
            elif choice == "2":
                self.menu_routes()
            elif choice == "3":
                try:
                    self.db_init()
                    print("БД успешно пересоздана! Загружены исходные данные.")
                except Exception as e:
                    print(f"Ошибка при инициализации БД: {e}")
            elif choice == "9":
                print("Программа завершена!")
                break
            else:
                print("Неверный ввод. Выберите пункт из предлагаемых.")


    def menu_stations(self):
        """Меню управления станциями."""
        page = 0
        while True:
            try:
                st = StationsTable()
                total = st.count()
                total_pages = max(1, (total + self.page_size - 1) // self.page_size)
                stations = st.page(self.page_size, page * self.page_size)
            except Exception as e:
                print(f"Ошибка подключения к БД: {e}")
                break
            print(f"--- СТАНЦИИ (Стр. {page+1} из {total_pages}) ---")
            print(f"{'№':<4} | {'Название':<25} | {'Зона':<6} | {'Номер':<5}")
            print("-" * 50)
            for i, row in enumerate(stations):
                display_num = page * self.page_size + i + 1
                print(f"{display_num:<4} | {row[1]:<25} | {row[2]:<6} | {row[3]:<5}")
            print("[N] Вперед, [P] Назад, [A] Добавить, [E] Изменить, [D] Удалить, [0] Назад")
            cmd = input("=> ").strip().lower()
            if cmd == "0":
                break
            elif cmd == "n" and page < total_pages - 1:
                page += 1
            elif cmd == "p" and page > 0:
                page -= 1
            elif cmd == "a":
                self.add_station()
            elif cmd == "e":
                self.edit_station(total)
            elif cmd == "d":
                self.delete_station(total)


    def add_station(self):
        """Добавление станции."""
        name = input("Название (0 - отмена): ").strip()
        if name == "0":
            return
        if not name:
            return print("Ошибка: название не может быть пустым!")
        zone = self.get_safe_int("Тарифная зона (>=0): ", min_val=0)
        num = self.get_safe_int("Порядковый номер (>0): ", min_val=1)
        try:
            StationsTable().insert_one([name, zone, num])
            print("Станция успешно добавлена!")
        except Exception as e:
            print(f"Ошибка БД: {e}")


    def edit_station(self, total):
        """Изменение станции."""
        num = self.get_safe_int(f"Номер строки для изменения (1-{total}, 0 - отмена): ", min_val=0, max_val=total, allow_cancel=True)
        if num == 0:
            return
        try:
            station = StationsTable().find_by_position(num)
            if not station:
                return print("Не найдено!")
            name = input(f"Название ({station[1]}): ").strip() or station[1]
            zone_str = input(f"Зона ({station[2]}): ").strip()
            zone = int(zone_str) if zone_str else station[2]
            num_str = input(f"Номер ({station[3]}): ").strip()
            s_num = int(num_str) if num_str else station[3]
            StationsTable().update_one(station[0], [name, zone, s_num])
            print("Станция обновлена!")
        except ValueError:
            print("Ошибка: зона и номер должны быть числами!")
        except Exception as e:
            print(f"Ошибка БД: {e}")


    def delete_station(self, total):
        """Удаление станции."""
        num = self.get_safe_int(f"Номер строки для удаления (1-{total}, 0 - отмена): ", min_val=0, max_val=total, allow_cancel=True)
        if num == 0:
            return
        try:
            station = StationsTable().find_by_position(num)
            if station:
                StationsTable().delete_one(station[0])
                print("Станция удалена!")
        except Exception as e:
            print(f"Ошибка при удалении: {e}")


    def menu_routes(self):
        """Просмотр выбранной станции."""
        try:
            st = StationsTable()
            total = st.count()
            if total == 0:
                return print("Сначала добавьте станции!")
            all_stations = st.all()
        except Exception as e:
            return print(f"Ошибка БД: {e}")
        print("Выберите станцию (введите номер, 0 - отмена):")
        for i, row in enumerate(all_stations):
            print(f"{i+1}. {row[1]}")
        num = self.get_safe_int("=> ", min_val=0, max_val=total, allow_cancel=True)
        if num == 0:
            return
        station = st.find_by_position(num)
        if station:
            self.route_actions(station)


    def route_actions(self, station):
        """Меню управления поездами конкретной станции."""
        while True:
            try:
                routes = RoutesTable().all_by_station(station[0])
            except Exception as e:
                print(f"Ошибка БД: {e}")
                break
            print(f"--- ПОЕЗДА СТАНЦИИ: {station[1]} ---")
            if not routes:
                print("Нет поездов.")
            else:
                print(f"{'№':<4} | {'Поезд':<8} | {'Откуда':<20} | {'Куда':<20} | {'Дни'}")
                print("-" * 70)
                for i, r in enumerate(routes):
                    print(f"{i+1:<4} | {r[1]:<8} | {r[2]:<20} | {r[3]:<20} | {r[4]}")
            print("[A] Добавить, [E] Изменить, [D] Удалить, [0] Назад")
            cmd = input("=> ").strip().lower()
            if cmd == "0":
                break
            elif cmd == "a":
                self.add_route()
            elif cmd == "e":
                self.edit_route(routes)
            elif cmd == "d":
                self.delete_route(routes)


    def add_route(self):
        """Добавление нового поезда, маршрута."""
        train = input("Номер поезда (0 - отмена): ").strip()
        if train == "0":
            return
        if not train:
            return print("Ошибка: номер не может быть пустым!")
        try:
            st = StationsTable()
            total = st.count()
            all_stations = st.all()
        except Exception as e:
            return print(f"Ошибка БД: {e}")
        print("Доступные станции:")
        for i, row in enumerate(all_stations):
            print(f"{i+1}. {row[1]}")
        start_num = self.get_safe_int("Начальная станция (номер): ", min_val=1, max_val=total)
        start = st.find_by_position(start_num)
        end_num = self.get_safe_int("Конечная станция (номер): ", min_val=1, max_val=total)
        end = st.find_by_position(end_num)
        if start[0] == end[0]:
            return print("Ошибка: начальная и конечная станции не могут совпадать!")
        days = input("Дни (1-7): ").strip()
        try:
            RoutesTable().insert_one([train, start[0], end[0], days])
            print("Поезд успешно добавлен!")
        except Exception:
            print("Ошибка БД: проверьте правильность ввода дней недели.")


    def edit_route(self, routes):
        """Изменение данных маршрута."""
        num = self.get_safe_int(f"Номер строки для изменения (1-{len(routes)}, 0 - отмена): ", min_val=0, max_val=len(routes), allow_cancel=True)
        if num == 0:
            return
        r = routes[num-1]
        train = input(f"Номер поезда ({r[1]}): ").strip() or r[1]
        days = input(f"Дни ({r[4]}): ").strip() or r[4]
        try:
            cur = self.connection.conn.cursor()
            sql = f"UPDATE {self.connection.prefix}route SET train_number=%s, route_days=%s WHERE id=%s"
            cur.execute(sql, (train, days, r[0]))
            self.connection.conn.commit()
            print("Поезд обновлен!")
        except Exception:
            print("Ошибка БД: проверьте правильность ввода дней недели.")


    def delete_route(self, routes):
        """Удаление маршрута."""
        num = self.get_safe_int(f"Номер строки для удаления (1-{len(routes)}, 0 - отмена): ", min_val=0, max_val=len(routes), allow_cancel=True)
        if num == 0:
            return
        try:
            cur = self.connection.conn.cursor()
            cur.execute(f"DELETE FROM {self.connection.prefix}route WHERE id=%s", (routes[num-1][0],))
            self.connection.conn.commit()
            print("Поезд удален!")
        except Exception as e:
            print(f"Ошибка БД: {e}")


if __name__ == "__main__":
    m = Main()
    m.main_cycle()