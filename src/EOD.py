#!/usr/bin/env python

import os
import sys
import time
import calendar 
import redis

SENSOR_STREAM = "DHT11-stream"
STAT_STREAM = "EOD-stream"

def get_redis_passwd():
    try:
        redis_passwd = os.environ['REDIS_PASSWD']
    except KeyError:
        print("Please provide REDIS_PASSWD to connect to redis")
        sys.exit(1)

    return redis_passwd


def get_day_data(redis_connection):
    midnight = time.strptime(time.strftime("%a, %d %b %Y 00:00:00 +0000", time.gmtime()), "%a, %d %b %Y %H:%M:%S +0000")
    eod = time.strptime(time.strftime("%a, %d %b %Y 23:59:59 +0000", time.gmtime()), "%a, %d %b %Y %H:%M:%S +0000")
    midnight_epoch = int(calendar.timegm(midnight))
    eod_epoch = int(calendar.timegm(eod))
    print(midnight_epoch)
    print(eod_epoch)
    #day_readings = redis_connection.xrevrange(STREAM, count=24 * 60, max=u'+', min=u'-')

r=redis.StrictRedis(host='localhost', port=6379, db=0, password=get_redis_passwd(), socket_timeout=10000, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)
get_day_data(r)
