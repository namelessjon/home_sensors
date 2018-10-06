from mitemp_bt.mitemp_bt_poller import MiTempBtPoller
from btlewrap.bluepy import BluepyBackend
import time
import logging
import psycopg2
import os

logger = logging.getLogger('mitemp_scan')

def _write_one_sensor_reading(cursor, sensor, reading_type, reading):
    cursor.execute("INSERT INTO sensor_readings(time, sensor_id, measure_type, reading) VALUES (NOW(), %s, %s, %s)", (sensor, reading_type, reading))


def _write_many_sensor_readings(cursor, sensor, readings):
    for (t, reading) in readings.items():
        _write_one_sensor_reading(cursor, sensor, t, reading)

def _find_sensor(cursor, sensor_name):
    id = cursor.execute("SELECT id FROM sensors WHERE sensor = %s",
            (sensor_name,))
    id = cursor.fetchone()
    return id

def write_readings(connection_string, sensor_name, readings):
    try:
        conn = psycopg2.connect(connection_string)
        with conn, conn.cursor() as cur:
            sensor = _find_sensor(cur, sensor_name)
            _write_many_sensor_readings(cur, sensor, readings)
    finally:
        conn.close()



poller = MiTempBtPoller('4C:65:A8:D4:F6:CE', BluepyBackend)

with open("mitemp.log", "a", buffering = 1) as f:
    while True:
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        try:
            temp = poller.parameter_value('temperature')
            humid = poller.parameter_value('humidity')
            battery = poller.parameter_value('battery')
        except:
            logger.error("Failed to connect to sensor")
            time.sleep(60)
            continue

        tsv = "%s\t%5.5g\t%5.5g\t%5.5g" % (timestamp, temp, humid, battery)
        print(tsv)
        f.write("%s\n" % (tsv,))
        try:
            write_readings(os.environ.fetch("DB_CONNECTION"),
                "xaomi-4C:65:A8:D4:F6:CE",
                {'temperature': temp, 'humidity': humid, 'battery': battery})
        except:
            logger.exception("Failed to write to DB")

        time.sleep(60*5)

