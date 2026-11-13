-- Выполнил: Кузнецов Кирилл. Група М26-555.
-- Вариант 6.
-- Описание предметной области. Описание расписания пригородных электропоездов одного направления. Включает в себя: станции, график движения электропоездов, стоимости билетов. Станции описываются: названием, тарифной зоной, порядковым номером на направлении. 
-- График движения электропоездов описывается: указанием станции начала маршрута, указанием станции, завершающей маршрут, списком станций, на которых поезд не останавливается, временем прибытия на каждую станцию, на которой поезд останавливается, списком дней недели, по которым данный маршрут работает. 
-- Стоимости билетов описываются: количеством пересекаемых зон и, непосредственно, самой стоимостью.
-- Поезда двигаются в одном направлении, но по мере удаления от начальной станции ветка может разделяться на несколько подветок. 
-- Выберите станции (или их идентификаторы, если другой информации нет в таблице), на которых поезда останавливаются в период с 14:00 до 15:00, отсортировав их по комбинации полей: станция (идентификатор) по возрастанию, время прибытия по убыванию.
-- Сопоставьте дням недели количество поездов, останавливающихся на станции «Москворечье». 



-- Очистка базы данных
DROP TABLE IF EXISTS without_stop CASCADE;
DROP TABLE IF EXISTS stop_route CASCADE;
DROP TABLE IF EXISTS route CASCADE;
DROP TABLE IF EXISTS stations CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;

-- Таблица тарифов. Пересекаемые зоны + цена билета.
CREATE TABLE tickets (
	travel_zones integer PRIMARY KEY CHECK (travel_zones >= 0),
	ticket_price numeric(10,2) NOT NULL CHECK (ticket_price >= 0.00)
);

-- Таблица станций. Номер станции, наименовании станции, тарифная зона, порядковый номер станции по направлению, станция-развилка.
CREATE TABLE stations (
    station_id serial PRIMARY KEY,
	station_name varchar(100) NOT NULL,
	tariff_zone integer NOT NULL CHECK (tariff_zone >= 0),
	station_number integer NOT NULL CHECK (station_number > 0),
	parent_station_id integer REFERENCES stations(station_id),
    -- Проверка, что станция не может быть развилкой самой себя
	CONSTRAINT uniq_station CHECK (parent_station_id <> station_id)
);

-- Таблица маршрутов. Код маршрута, наименование поезда, начальная станция, конченая станция, расписание.
CREATE TABLE route (
    route_id serial PRIMARY KEY,
	train_number varchar(20) NOT NULL,
	start_station_id integer NOT NULL REFERENCES stations(station_id),
	end_station_id integer NOT NULL REFERENCES stations(station_id),
	route_days varchar(20) NOT NULL CHECK (route_days ~ '^[1-7](,[1-7])*$'),
	-- Проверка, что начальная и конченая станция не совпадают
	CONSTRAINT check_stations CHECK (start_station_id <> end_station_id)
);

-- Таблица остановок. Номер станции остановки, маршрут, номер станции, время прибытия.
CREATE TABLE stop_route (
    stop_id serial PRIMARY KEY,
	route_id integer NOT NULL REFERENCES route(route_id) ON DELETE CASCADE,
	station_id integer NOT NULL REFERENCES stations(station_id),
	route_time time NOT NULL,
	-- Проверка, что поезд не может останавливаться на одной и той же станции на маршруте.
	CONSTRAINT unique_route_station_s UNIQUE (route_id, station_id) 
);

-- Таблица пропусков. Номер пропуска, номер маршрута, номер станции.
CREATE TABLE without_stop (
    skip_id serial PRIMARY KEY,
	route_id integer NOT NULL REFERENCES route(route_id) ON DELETE CASCADE,
	station_id integer NOT NULL REFERENCES stations(station_id),
	-- Проверка, что поезд не может пропустить одну и ту же станцию на маршруте.
	CONSTRAINT unique_route_station_w UNIQUE (route_id, station_id) 
);

-- Заполнение тарифов.
INSERT INTO tickets (travel_zones, ticket_price) VALUES
(1, 50.00),
(2, 100.00),
(3, 150.00),
(4, 200.00),
(5, 250.00),
(6, 300.00);

-- Заполнение станций.
INSERT INTO stations (station_name, tariff_zone, station_number, parent_station_id) VALUES
('Иглино', 6, 1, NULL),
('Тауш', 5, 2, NULL),
('Индустриальный парк', 4, 3, NULL),
('Шакша', 3, 4, NULL),
('Спортивная', 2, 5, NULL),
('Москворечье', 1, 6, NULL),
('Черниковка', 1, 7, NULL),
('Парковая', 1, 8, NULL),
('Воронки', 1, 9, NULL),
('Уфа', 1, 10, NULL);

-- Заполнение маршрутов.
INSERT INTO route (train_number, start_station_id, end_station_id, route_days) VALUES
('1000', 1, 10, '1,2,3,4,5,6,7'),
('1001', 1, 7, '1,2,3,4,5'),
('1002', 1, 8, '1,2,3,4,5,6,7'),
('1003', 1, 9, '1,2,3,4,5'),
('1004', 2, 6, '1,2,3,4,5,6,7'),
('1005', 2, 4, '1,3,5,7'),
('1006', 2, 3, '2,3,4,5'),
('1007', 3, 10, '1,2,3,4,5,6'),
('1008', 3, 10, '2,4,6'),
('1009', 3, 9, '1,2,3,4,5'),
('2000', 4, 10, '1,2,3,4,5'),
('2001', 4, 8, '1,2,3,4,5,7'),
('2002', 4, 7, '1,2,3,4,7'),
('2003', 4, 10, '1,2,3,4,5');

-- Заполнение остановок.
INSERT INTO stop_route (route_id, station_id, route_time) VALUES
-- Маршрут 1.
(1, 1, '13:30:00'),
(1, 2, '13:35:00'),
(1, 6, '13:55:00'),
(1, 7, '14:00:00'),
(1, 8, '14:05:00'),
(1, 9, '14:10:00'),
(1, 10, '14:15:00'),
-- Маршрут 2.
(2, 1, '14:00:00'),
(2, 2, '14:05:00'),
(2, 3, '14:10:00'),
(2, 5, '14:20:00'),
(2, 6, '14:25:00'),
(2, 7, '14:30:00'),
-- Маршрут 3.
(3, 1, '14:10:00'),
(3, 2, '14:15:00'),
(3, 4, '14:25:00'),
(3, 8, '14:45:00'),
-- Маршрут 4.
(4, 1, '14:20:00'),
(4, 3, '14:30:00'),
(4, 4, '14:35:00'),
(4, 7, '14:50:00'),
(4, 9, '15:00:00'),
-- Маршрут 5.
(5, 2, '14:30:00'),
(5, 3, '14:35:00'),
(5, 4, '14:40:00'),
(5, 5, '14:45:00'),
(5, 6, '14:50:00'),
-- Маршрут 6.
(6, 2, '15:00:00'),
(6, 3, '15:10:00'),
(6, 4, '15:20:00'),
-- Маршрут 7.
(7, 2, '15:30:00'),
(7, 3, '15:40:00'),
-- Маршрут 8.
(8, 3, '15:50:00'),
(8, 4, '15:55:00'),
(8, 5, '16:00:00'),
(8, 6, '16:05:00'),
(8, 7, '16:10:00'),
(8, 8, '16:15:00'),
(8, 9, '16:20:00'),
(8, 10, '16:25:00'),
-- Маршрут 9.
(9, 3, '16:30:00'),
(9, 5, '16:40:00'),
(9, 7, '16:50:00'),
(9, 9, '17:00:00'),
-- Маршрут 10.
(10, 3, '17:10:00'),
(10, 4, '17:15:00'),
(10, 6, '17:25:00'),
(10, 8, '17:35:00'),
(10, 10, '17:45:00'),
-- Маршрут 11.
(11, 4, '17:50:00'),
(11, 5, '17:55:00'),
(11, 6, '18:00:00'),
(11, 7, '18:05:00'),
(11, 8, '18:10:00'),
(11, 10, '18:20:00'),
-- Маршрут 12.
(12, 4, '18:30:00'),
(12, 5, '18:35:00'),
(12, 6, '18:40:00'),
(12, 8, '18:50:00'),
-- Маршрут 13.
(13, 4, '19:00:00'),
(13, 5, '19:05:00'),
(13, 6, '19:10:00'),
(13, 7, '19:15:00'),
-- Маршрут 14.
(14, 4, '19:30:00'),
(14, 6, '19:40:00'),
(14, 8, '19:50:00'),
(14, 10, '20:00:00');

-- Заполнение пропусков.
INSERT INTO without_stop (route_id, station_id) VALUES
(1, 4),
(2, 4),
(3, 6),
(4, 6),
(1, 5),
(1, 3);

-- Станции, где поезда останавливаются с 14:00 до 15:00.
SELECT s.station_id, s.station_name, sr.route_time
FROM stop_route sr
JOIN stations s ON sr.station_id = s.station_id
WHERE sr.route_time >= '14:00:00' AND sr.route_time <= '15:00:00'
ORDER BY s.station_id ASC, sr.route_time DESC;

-- Количество станций на каждом маршруте.
SELECT r.train_number, COUNT(sr.station_id) AS stations_count
FROM route r
JOIN stop_route sr ON r.route_id = sr.route_id
GROUP BY r.train_number
ORDER BY stations_count DESC;

-- Количество поездов, останавливающихся на станции 'Москворечье'.
SELECT 
COUNT(CASE WHEN r.route_days LIKE '%1%' THEN 1 END) AS "Понедельник",
COUNT(CASE WHEN r.route_days LIKE '%2%' THEN 1 END) AS "Вторник",
COUNT(CASE WHEN r.route_days LIKE '%3%' THEN 1 END) AS "Среда",
COUNT(CASE WHEN r.route_days LIKE '%4%' THEN 1 END) AS "Четверг",
COUNT(CASE WHEN r.route_days LIKE '%5%' THEN 1 END) AS "Пятница",
COUNT(CASE WHEN r.route_days LIKE '%6%' THEN 1 END) AS "Суббота",
COUNT(CASE WHEN r.route_days LIKE '%7%' THEN 1 END) AS "Воскресенье"
FROM route r
JOIN stop_route sr ON r.route_id = sr.route_id
JOIN stations s ON sr.station_id = s.station_id
WHERE s.station_name = 'Москворечье';

-- Проверка структуры.
select * from tickets;
select * from stations;
select * from route;
select * from stop_route;
select * from without_stop;