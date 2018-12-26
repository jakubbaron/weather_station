#!/usr/bin/env python

# WS server that sends messages at random intervals

import os
import sys
import asyncio
import websockets
import redis

STREAM = {"DHT11-stream": "$"}

def get_redis_passwd():
    try:
        redis_passwd = os.environ['REDIS_PASSWD']
    except KeyError:
        print("Please provide REDIS_PASSWD to connect to redis")
        sys.exit(1)

    return redis_passwd

r=redis.StrictRedis(host='localhost', port=6379, db=0, password=get_redis_passwd(), socket_timeout=10000, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

async def time(websocket, path):
    while True:
        last_data = r.xread(STREAM, block=0)
        print(str(last_data))
        await websocket.send(str(last_data))

start_server = websockets.serve(time, '192.168.0.123', 5678)


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
