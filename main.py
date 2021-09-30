from discord import bot
import requests
import os

urlBase = "https://discord.com/api/v8"
bot = bot.Bot()

token = os.environ['DISCORD_TOKEN']


@bot.event
async def on_message_create(data):
    payload = {
        "content": "Hello, World!",
        "tts": False,
        }
    headers = {
        "Authorization": f"Bot {token}"
    }
    # r = await requests.get(urlBase + "/channels/887377482741862404")
    print("it worky??")
    try:
        if data["author"]["bot"]:
            return
    except:
        pass
    r = requests.post(urlBase + "/channels/887377482741862404/messages", json=payload, headers=headers)
    print(r)

bot.start()