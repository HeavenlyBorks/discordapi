import discord
import requests
import os

urlBase = "https://discord.com/api/v8"
bot = discord.Bot()

token = os.environ['DISCORD_TOKEN']


@bot.event
async def on_message_create(data):
    payload = {
        "content": "Hello, World!",
        "tts": False,
        }
    # r = await requests.get(urlBase + "/channels/887377482741862404")
    try:
        if "bot" in data["author"]:
            return
    except:
        pass
    # r = requests.post(urlBase + "/channels/887377482741862404/messages", json=payload, headers=headers)
    # print(r)
    r = discord.request("POST", "/channels/887377482741862404/messages", payload, token)

bot.start()