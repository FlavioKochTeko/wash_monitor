import csv
from datetime import datetime
import time


class FakeSensor:
    def __init__(self, filename, speed=100.0):
        """
        speed = 1 → echte Geschwindigkeit
        speed = 10 → 10x schneller
        speed = 100 → 100x schneller
        """
        self.file = open(filename, "r")
        self.reader = csv.DictReader(self.file, delimiter=";")

        self.last_time = None
        self.speed = speed

    def read(self):
        try:
            row = next(self.reader)

            timestamp = datetime.strptime(row["Zeit"], "%d.%m.%Y %H:%M:%S")
            power = float(row["Leistung"])

            if self.last_time is not None:
                diff = (timestamp - self.last_time).total_seconds()

                # Geschwindigkeit anpassen
                time.sleep(diff / self.speed)

            self.last_time = timestamp

            return power

        except StopIteration:
            return None
