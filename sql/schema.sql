BEGIN;

    CREATE TYPE measure_type_t AS ENUM('temperature', 'humidity', 'battery');

    CREATE TABLE sensors(
        id SERIAL PRIMARY KEY,
        sensor VARCHAR(32) NOT NULL,
        sensor_alias VARCHAR(32),
        measure_types measure_type_t[] NOT NULL
    );

    CREATE TABLE sensor_readings(
        time timestamp with time zone NOT NULL,
        sensor_id integer NOT NULL,
        measure_type measure_type_t NOT NULL,
        reading NUMERIC(5, 2) NOT NULL,
        FOREIGN KEY (sensor_id) REFERENCES sensors(id)
    );
    CREATE INDEX sensor_time ON sensor_readings USING BRIN (time);


    CREATE TABLE sensor_locations(
        name VARCHAR(32) NOT NULL,
        sensor_id integer NOT NULL,
        time_from timestamp with time zone NOT NULL,
        time_to   timestamp with time zone,
        FOREIGN KEY (sensor_id) REFERENCES sensors(id)
    );
COMMIT;
