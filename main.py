import asyncio
from client import Client

if __name__ == '__main__':
    # Creating client object
    client = Client()
    loop = asyncio.get_event_loop()
    # Start connection and get client connection protocol
    connection = loop.run_until_complete(client.start(loop))
    # Start listener and heartbeat 
    tasks = [
        asyncio.ensure_future(client.heartbeat(connection)),
        asyncio.ensure_future(client.listen(connection))
    ]

    loop.run_until_complete(asyncio.wait(tasks))