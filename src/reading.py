#!/usr/bin/python
# https://codereview.stackexchange.com/a/156404
# Thanks @alecxe - https://codereview.stackexchange.com/users/24208/alecxe
import time

import Adafruit_DHT
from collections import namedtuple

Stats = namedtuple("Stats", ["average", "min", "max"])

SENSOR = Adafruit_DHT.DHT11
GPIO = 4
MEASUREMENTS_COUNT = 5

def get_stats(measurements):
    return Stats(average=sum(measurements) / float(len(measurements)),
                 min=min(measurements),
                 max=max(measurements))

if __name__ == '__main__':
    while True:
        filename = str(time.strftime("%Y%m%d", time.gmtime()))
        with open(filename, "a") as file:
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

            humidities = []
            temperatures = []
            for _ in range(MEASUREMENTS_COUNT):
                humidity, temperature = Adafruit_DHT.read_retry(SENSOR, GPIO)
                humidities.append(humidity)
                temperatures.append(temperature)

            message_template = "{date}: {th.average}, {th.min}, {th.max} | {tt.average}, {tt.min}, {tt.max}\n"
            file.write(message_template.format(date=date, th=get_stats(humidities), tt=get_stats(temperatures)))
