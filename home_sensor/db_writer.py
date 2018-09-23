import psycopg2

psycopg2.extensions.register_type(
    psycopg2.extensions.new_array_type(
        (16467,), 'measure_type_t[]', psycopg2.STRING))


class DBWriter(object):
    def __init__(self, connection_string, sensor_name):
        self.connection_string = connection_string
        self.sensor_name       = sensor_name

    def write(self, readings):
        try:
            conn = psycopg2.connect(self.connection_string)
            with conn, conn.cursor() as cur:
                sensor = _find_sensor(cur, self.sensor_name)
                _write_many_sensor_readings(cur, sensor, readings)
        finally:
            conn.close()

    def _write_one_sensor_reading(cursor, sensor, reading_type, reading):
        cursor.execute("""
        INSERT INTO
          sensor_readings(time, sensor_id, measure_type, reading)
        VALUES (NOW(), %s, %s, %s)""",
                       (sensor, reading_type, reading))

    def _write_many_sensor_readings(cursor, sensor, readings):
        for (t, reading) in readings.items():
            _write_one_sensor_reading(cursor, sensor, t, reading)

    def _find_sensor(cursor, sensor_name):
        id = cursor.execute("SELECT id FROM sensors WHERE sensor = %s",
                            (sensor_name,))
        id = cursor.fetchone()
        return id
