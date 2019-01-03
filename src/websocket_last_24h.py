#!/usr/bin/env python

# WS server that sends messages at random intervals

import os
import sys
import asyncio
import websockets
import redis
import functools
import json

STREAM = "DHT11-stream"

def get_redis_passwd():
    try:
        redis_passwd = os.environ['REDIS_PASSWD']
    except KeyError:
        print("Please provide REDIS_PASSWD to connect to redis")
        sys.exit(1)

    return redis_passwd


async def handler(websocket, path, redis_connection):
    last_day_readings = redis_connection.xrevrange(STREAM, count=24 * 60, max=u'+', min=u'-')
    sensor_data_arr = []
    for item in last_day_readings:
        sensor_data = {}
        str_data = {}
        for k,v in item[1].items():
            str_data[k.decode('utf-8')] = v.decode('utf-8')
        time_point = item[0].decode('utf-8')
        sensor_data_arr.append(str_data)
    sensor_data_arr.reverse()
    json_data = json.dumps(sensor_data_arr)
    await websocket.send(json_data)

r=redis.StrictRedis(host='localhost', port=6379, db=0, password=get_redis_passwd(), socket_timeout=10000, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

bound_handler = functools.partial(handler, redis_connection=r)
start_server = websockets.serve(bound_handler, host='192.168.1.224', port=5679)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

