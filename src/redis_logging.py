import os
import sys
import time
import redis

import sched, time

s = sched.scheduler(time.time, time.sleep)

def get_average(measurements):
    return str(sum(measurements)/float(len(measurements)))

def log_into_redis(r, stream, readings):
    print(r.xadd(stream, {'date': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), 'temperature': get_average(readings['temperatures']), 'humidity': get_average(readings['humidities'])}, maxlen=150000))

def do_something(sc, r, stream, readings): 
    print("Running")
    log_into_redis(r, stream, readings)
    s.enter(60, 1, do_something, (sc,r, stream, readings))

def get_redis_passwd():
    try:
        redis_passwd = os.environ['REDIS_PASSWD']
    except KeyError:
        print("Please provide REDIS_PASSWD to connect to redis")
        sys.exit(1)

    return redis_passwd

def main():

    r=redis.StrictRedis(host='localhost', port=6379, db=0, password=get_redis_passwd(), socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

    stream="DHT11-stream"
    humidities=[30,30,30,31,32]
    temperatures=[24,25,24,24,23]
    readings = {}
    readings['temperatures']=temperatures
    readings['humidities']=humidities
    s.enter(60, 1, do_something, (s, r, stream, readings))
    s.run()

if __name__ == "__main__":
    main()
