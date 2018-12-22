import os
import sys
import time
import redis

from collections import namedtuple
Stats = namedtuple("Stats", ["average", "min", "max"])

def get_redis_passwd():
    try:
        redis_passwd = os.environ['REDIS_PASSWD']
    except KeyError:
        print("Please provide REDIS_PASSWD to connect to redis")
        sys.exit(1)

    return redis_passwd

def get_stats(measurements):
    return Stats(average=sum(measurements) / float(len(measurements)),
                 min=min(measurements),
                 max=max(measurements))

def main():

    r=redis.StrictRedis(host='localhost', port=6379, db=0, password=get_redis_passwd(), socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

    stream="DHT11-stream"
    humidities=[30,30,30,31,32]
    temperatures=[24,25,24,24,23]
    message_template = "{th.average}, {th.min}, {th.max}"
    print(r.xadd(stream, {'date': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), 'temperature': message_template.format(th=get_stats(temperatures)), 'humidites': message_template.format(th=get_stats(humidities))}, maxlen=150000))

if __name__ == "__main__":
    main()
