BEGIN;
CREATE TABLE sensor_readings(
    time timestamp with time zone NOT NULL,
    sensor VARCHAR(32) NOT NULL,
    measure_type VARCHAR(32) NOT NULL,
    reading NUMERIC(5, 2) NOT NULL
);
CREATE INDEX sensor_time ON sensor_readings USING BRIN (time);

CREATE TABLE sensors(
    sensor VARCHAR(32) NOT NULL,
    measure_type VARCHAR(32) NOT NULL
);

CREATE TABLE sensor_locations(
    name VARCHAR(32) NOT NULL,
    sensor VARCHAR(32) NOT NULL,
    time_from timestamp with time zone NOT NULL,
    time_to   timestamp with time zone
);
COMMIT;
