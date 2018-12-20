import os
import sys
import redis

def get_redis_passwd():
    try:
        redis_passwd = os.environ['REDIS_PASSWD']
    except KeyError:
        print "Please provide REDIS_PASSWD to connect to redis"
        sys.exit(1)

    return redis_passwd

def main():

    r=redis.StrictRedis(host='localhost', port=6379, db=0, password=get_redis_passwd(), socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

    print r.get('cat')

if __name__ == "__main__":
    main()
