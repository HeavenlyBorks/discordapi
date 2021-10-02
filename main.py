import discord
import requests
import os

urlBase = "https://discord.com/api/v8"
bot = discord.Bot()

token = os.environ['DISCORD_TOKEN']

@bot.event
async def on_message_create(msg):
    try:
        if "bot" in msg.author:
            return
    except:
        pass
    msg.channel.send("Hello World")

bot.start(token)