import asyncio
import websockets
import random
import json
import os
from dotenv import load_dotenv
load_dotenv()

# INTERVAL = 1
# S = ""
# RESPONSE = ""
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
print(BOT_TOKEN)
wssURL = "wss://gateway.discord.gg/?v=8&encoding=json"

# app = Flask(__name__)
# prefix = "/api/interactions/"

# async def start(loop):
#   async with websockets.connect(wssURL) as WS:
#     global INTERVAL
#     global S
#     global RESPONSE
#     RESPONSE = await WS.recv()
#     RESPONSE = json.loads(RESPONSE)
#     INTERVAL = RESPONSE["d"]["heartbeat_interval"]
#     S = RESPONSE["s"]
#     # data = {
#     #   "op": 1,
#     #   "d": S
#     # }
#     # await WS.send(json.dumps(data))
#     identify_json = {
#       "op": 2,
#       "d": {
#         "token": f"{BOT_TOKEN}",
#         "intents": 513,
#         "properties": {
#           "$os": "linux",
#           "$browser": "my_library",
#           "$device": "my_library"
#         }
#       }
#     }
#     await WS.send(json.dumps(identify_json))
#     # r = await WS.recv()
#     print("done with start")
#     return WS

# async def listen(WS):
#     # print("listen")
#     while True:
#       try:
#         r = await WS.recv()
#         r = json.loads(r)
#         # print(r)
#         await asyncio.sleep(.1)
#         if r["op"] == 0:
#           print(r["t"])
#         elif r["op"] == 1:
#           ping(WS)
#       except websockets.exceptions.ConnectionClosedOK:
#         print("connection closed")
#         break

# async def ping(WS):
#     while True:
#       try:
#         global INTERVAL
#         global S
#         # print("ping")
#         data = {
#           "op": 1,
#           "d": S
#         }
#         await WS.send(json.dumps(data))
#         await asyncio.sleep(INTERVAL)
#       except websockets.exceptions.ConnectionClosedOK:
#         print("connection closed")

class Client():
  def __init__(self):
    pass
  
  async def start(self, loop):
    self.loop = loop
    self.connection = await websockets.connect(wssURL)
    response = await self.connection.recv()
    response = json.loads(response)
    print(response)
    self.interval = response["d"]["heartbeat_interval"]
    self.last_s = response["s"]
    data = {
      "op": 1,
      "d": self.last_s
    }
    await self.connection.send(json.dumps(data))
    self.identify_json = {
      "op": 2,
      "d": {
        "token": f"{BOT_TOKEN}",
        "intents": 513,
        "properties": {
          "$os": "linux",
          "$browser": "my_library",
          "$device": "my_library"
        }
      }
    }
    await self.connection.send(json.dumps(self.identify_json))
    print("done with start")
    return self.connection
  
  async def send(self, connection, message):
    """Sends a message to the server"""
    await connection.send(json.dumps(message))
  
  async def listen(self, connection):
    """Listens for messages from the server"""
    while True:
      try:
        message = await connection.recv()
        message = json.loads(message)
        op = message["op"]
        print('Received message from server: \n' + str(message))
        if op == 0:
          self.last_s = message["s"]
          title = message["t"]
          if title == "READY":
            self.last_id = message["d"]["session_id"]
        elif op == 1:
          await self.quick_heartbeat(connection)
        elif op == 9:
          await self.send(connection, json.dumps(self.identify_json))
        elif op == 10:
          self.interval = message["d"]["heartbeat_interval"]
      except websockets.exceptions.ConnectionClosed as e:
        print(str(e) + " - listen")
        break
  
  async def quick_heartbeat(self, connection):
    """send a single heartbeat with no interval"""
    try:
      data = {
        "op": 1,
        "d": self.last_s
      }
      await connection.send(json.dumps(data))
    except Exception as e:
      print(str(e) + ' - heartbeat quick')

  async def heartbeat(self, connection):
    """send a heartbeat every interval"""
    while True:
      try:
        data = {
          "op": 1,
          "d": self.last_s
        }
        await connection.send(json.dumps(data))
        await asyncio.sleep(self.interval/1000)
      except Exception as e:
        print(str(e) + ' - heartbeat')