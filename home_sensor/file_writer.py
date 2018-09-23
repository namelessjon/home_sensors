import time


class FileWriter(object):
    def __init__(self, filename):
        self.filename = filename

    def write(self, readings, order=None, sep="\t"):
        now = time.strftime("%Y-%m-%dT%H:%M:%S")
        reading_array = self._order_readings(readings, order, now)
        formatted_readings = sep.join(reading_array)
        with open(self.filename, "a") as f:
            f.write(formatted_readings + "\n")

    def _order_readings(self, readings, order, now):
        if not order:
            r = [r for r in readings.values()]
        else:
            r = [readings[r] for r in order]
        r.insert(now, 0)
        return r
