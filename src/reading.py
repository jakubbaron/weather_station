#!/usr/bin/python
# https://codereview.stackexchange.com/a/156404
# Thanks @alecxe - https://codereview.stackexchange.com/users/24208/alecxe
import os
import sys

import redis

import time
import Adafruit_DHT


def get_average(measurements):
    return str(sum(measurements)/float(len(measurements)))

def get_redis_passwd():
    try:
        redis_passwd = os.environ['REDIS_PASSWD']
    except KeyError:
        print("Please provide REDIS_PASSWD to connect to redis")
        sys.exit(1)

    return redis_passwd


if __name__ == '__main__':
    SENSOR = Adafruit_DHT.DHT11
    GPIO = 4
    MEASUREMENTS_COUNT = 60
    STREAM="DHT11-stream"
    MAXLEN=150000

    r=redis.StrictRedis(host='localhost', port=6379, db=0, password=get_redis_passwd(), socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

    while True:
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        humidities = []
        temperatures = []
        for _ in range(MEASUREMENTS_COUNT):
            humidity, temperature = Adafruit_DHT.read_retry(SENSOR, GPIO)
            humidities.append(humidity)
            temperatures.append(temperature)

        data = {}
        data['date'] = date
        data['temperature'] = get_average(temperatures)
        data['humidity'] = get_average(humidities)
        r.xadd(STREAM, data, maxlen=MAXLEN)
