#!/usr/bin/python
# https://codereview.stackexchange.com/a/156404
# Thanks @alecxe - https://codereview.stackexchange.com/users/24208/alecxe
import os
import sys

import redis

import sched, time
import Adafruit_DHT

SENSOR = Adafruit_DHT.DHT11
GPIO = 4
MEASUREMENTS_COUNT = 50
STREAM = "DHT11-stream"
MAXLEN = 0#150000

SCHEDULER = sched.scheduler(time.time, time.sleep)

def get_average(measurements):
    return str(sum(measurements)/float(len(measurements)))

def get_redis_passwd():
    try:
        redis_passwd = os.environ['REDIS_PASSWD']
    except KeyError:
        print("Please provide REDIS_PASSWD to connect to redis")
        sys.exit(1)

    return redis_passwd

def get_readings(scheduler, r):
    scheduler.enter(60, 0, get_readings, (scheduler, r,))

    humidities = []
    temperatures = []

    for _ in range(MEASUREMENTS_COUNT):
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, GPIO)
        humidities.append(humidity)
        temperatures.append(temperature)

    data = {}
    data['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    data['temperature'] = get_average(temperatures)
    data['humidity'] = get_average(humidities)
    data['sensor'] = 'DHT11-main'
    r.xadd(STREAM, data, maxlen=MAXLEN)
    

if __name__ == '__main__':

    r=redis.StrictRedis(host='localhost', port=6379, db=0, password=get_redis_passwd(), socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

    SCHEDULER.enter(60, 0, get_readings, (SCHEDULER, r,))
    SCHEDULER.run()
