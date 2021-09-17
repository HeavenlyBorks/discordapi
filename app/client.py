import asyncio
import websockets
import random
import json
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
print(BOT_TOKEN)
wssURL = "wss://gateway.discord.gg/?v=8&encoding=json"

class Client():
  def __init__(self, json=False):
    self.json_v = json
  
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
        pretty_message = json.dumps(message, indent=2)
        op = message["op"]
        print('Received message from server: \n' + str(pretty_message))
        if op == 0:
          self.last_s = message["s"]
          title = message["t"]
          # on_ready
          if title == "READY":
            if self.json_v:
              with open("json/ready.json", "w", encoding="utf-8") as f:
                json.dump(message, f, ensure_ascii=False, indent=2)
            self.last_id = message["d"]["session_id"]
          # on_message
          elif title == "MESSAGE_CREATE":
            if self.json_v:
              with open("json/message_create.json", "w", encoding="utf-8") as f:
                json.dump(message, f, ensure_ascii=False, indent=2)
          # on_interaction
          elif title == "INTERACTION_CREATE":
            if self.json_v:
              with open("json/interaction_create.json", "w", encoding="utf-8") as f:
                json.dump(message, f, ensure_ascii=False, indent=2)
          # on_guild_create
          elif title == "GUILD_CREATE":
            if self.json_v:
              with open("json/guild_create.json", "w", encoding="utf-8") as f:
                json.dump(message, f, ensure_ascii=False, indent=2)
        elif op == 1:
          await self.quick_heartbeat(connection)
        elif op == 9:
          await self.send(connection, json.dumps(self.identify_json))
        elif op == 10:
          self.interval = message["d"]["heartbeat_interval"]
      except Exception as e:
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