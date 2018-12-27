#!/usr/bin/env python

# WS server that sends messages at random intervals

import os
import sys
import asyncio
import websockets
import redis
import functools
import json

STREAM = {"DHT11-stream": "$"}

def get_redis_passwd():
    try:
        redis_passwd = os.environ['REDIS_PASSWD']
    except KeyError:
        print("Please provide REDIS_PASSWD to connect to redis")
        sys.exit(1)

    return redis_passwd


async def handler(websocket, path, redis_connection):
  last_reading = r.xrevrange(STREAM, count=1, max=u'+', min=u'-')
  time_point, read_data = last_reading[0]
  time_point = time_point.decode('utf-8')
  str_data = {}
  for k,v in read_data.items():
      str_data[k.decode('utf-8')] = v.decode('utf-8')
  sensor_data = {"stream_name" : STREAM,
                 "data": str_data,
                 "time_point": time_point }
  json_data = json.dumps(sensor_data)
  await websocket.send(json_data)

r=redis.StrictRedis(host='localhost', port=6379, db=0, password=get_redis_passwd(), socket_timeout=10000, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)
bound_handler = functools.partial(handler, redis_connection=r)
start_server = websockets.serve(bound_handler, host='192.168.0.123', port=5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
