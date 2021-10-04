import asyncio
import discord
import sys
import json
import traceback
import requests

__all__ = (
    "Bot",
)

class Bot():
    def __init__(self):
        pass
    # event maker
    def event(self, coro):
        setattr(self, coro.__name__[3:].upper(), coro)
        return coro

    def start(self, token):
        # Creating client object
        gateway = discord.Gateway(json=True) if sys.argv[0] == True else discord.Gateway()
        loop = asyncio.get_event_loop()
        discord.set_globals(token, self, loop)
        # Start connection and get client connection protocol
        connection = loop.run_until_complete(gateway.start(loop))
        # Start listener and heartbeat 
        tasks = [
            asyncio.ensure_future(gateway.heartbeat(connection)),
            asyncio.ensure_future(self.listen(connection))
        ]

        loop.run_until_complete(asyncio.wait(tasks))
    
    # event listener
    async def listen(self, connection):  # sourcery no-metrics
        while True:
            try:
                message = await connection.recv()
                message = json.loads(message)
                pretty_message = json.dumps(message, indent=2)
                op = message["op"]
                print('Received message from server: \n' + str(pretty_message))
                if op == 0:
                    self.last_s = message["s"]
                    title = str(message["t"])
                    if hasattr(self, title):
                        await getattr(self, "_" + title)(message["d"])
                    # on_ready
                    # if title == "READY":
                    #     if self.json_v:
                    #         with open("json/ready.json", "w", encoding="utf-8") as f:
                    #             json.dump(message, f, ensure_ascii=False, indent=2)
                    #     self.last_id = message["d"]["session_id"]
                    #     if message["d"]["user"]["bot"]:
                    #         self.user = discord.bot.Bot(message["d"]["user"])
                    #     else:
                    #         self.user = discord.user.User(message["d"]["user"])
                    # # on_message
                    # elif title == "MESSAGE_CREATE":
                    #     if self.json_v:
                    #         with open("json/message_create.json", "w", encoding="utf-8") as f:
                    #             json.dump(message, f, ensure_ascii=False, indent=2)
                    # # on_interaction
                    # elif title == "INTERACTION_CREATE":
                    #     if self.json_v:
                    #         with open("json/interaction_create.json", "w", encoding="utf-8") as f:
                    #             json.dump(message, f, ensure_ascii=False, indent=2)
                    #     inter = discord.interaction.Interaction(message["d"])
                    #     url = f"https://discord.com/api/v8/interactions/{inter.id}/{inter.token}/callback"
                    #     i_json = {
                    #         "type": 4,
                    #         "data": {
                    #             "content": "High Five!"
                    #         }
                    #     }
                    #     r = requests.post(url, json=i_json)
                    # # on_guild_create
                    # elif title == "GUILD_CREATE":
                    #     if self.json_v:
                    #         with open("json/guild_create.json", "w", encoding="utf-8") as f:
                    #             json.dump(message, f, ensure_ascii=False, indent=2)
                    #     guild = discord.guild.Guild(message["d"])
                    #     self.guilds.append(guild)
                elif op == 1:
                    await self.quick_heartbeat(connection)
                elif op == 9:
                    await self.send(connection, json.dumps(self.identify_json))
                elif op == 10:
                    self.interval = message["d"]["heartbeat_interval"]
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                print(e)
                print("- listen")
                break

    # [---
    #      OP code 0 interactions
    #                             ---]
    async def _MESSAGE_CREATE(self, data):
        msg = discord.Message(data)
        await self.MESSAGE_CREATE(msg)