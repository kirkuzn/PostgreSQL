-- Выполнил: Кузнецов Кирилл. Група М26-555.
-- Вариант 6.
-- Описание предметной области. Описание расписания пригородных электропоездов одного направления. Включает в себя: станции, график движения электропоездов, стоимости билетов. Станции описываются: названием, тарифной зоной, порядковым номером на направлении. 
-- График движения электропоездов описывается: указанием станции начала маршрута, указанием станции, завершающей маршрут, списком станций, на которых поезд не останавливается, временем прибытия на каждую станцию, на которой поезд останавливается, списком дней недели, по которым данный маршрут работает. 
-- Стоимости билетов описываются: количеством пересекаемых зон и, непосредственно, самой стоимостью.
-- Поезда двигаются в одном направлении, но по мере удаления от начальной станции ветка может разделяться на несколько подветок. 

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

-- Проверка структуры.
select * from tickets;
select * from stations;
select * from route;
select * from stop_route;
select * from without_stop;