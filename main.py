import sys
import asyncio
import discord

if __name__ == '__main__':
    # Creating client object
    gateway = discord.gateway.Gateway(json=True) if sys.argv[0] == True else discord.gateway.Gateway()
    loop = asyncio.get_event_loop()
    # Start connection and get client connection protocol
    connection = loop.run_until_complete(gateway.start(loop))
    # Start listener and heartbeat 
    tasks = [
        asyncio.ensure_future(gateway.heartbeat(connection)),
        asyncio.ensure_future(gateway.listen(connection))
    ]

    loop.run_until_complete(asyncio.wait(tasks))