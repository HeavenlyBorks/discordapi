# example bot for now - this example will showcase stuff that is functional atm
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
    await msg.channel.send(f"{msg.content}? more like joe mama")

bot.start(token)