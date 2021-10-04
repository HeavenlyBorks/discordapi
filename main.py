# example bot for now - this example will showcase stuff that is functional atm
import discord
import requests
import os
import asyncio

urlBase = "https://discord.com/api/v8"
bot = discord.Bot()

token = os.environ['DISCORD_TOKEN']

@bot.event
async def on_message_create(msg: discord.Message):
    try:
        if "bot" in msg.author:
            return
    except:
        pass
    funny = await msg.channel.send(f"{msg.content}? more like ur fat")
    await asyncio.sleep(3)
    haha = await funny.edit("oh sorry i didn't mean it like that")
    await asyncio.sleep(3)
    await funny.delete()


bot.start(token)