import discord
import asyncio
import websockets
import random
import json
import os
import time
import requests
import traceback

wssURL = "wss://gateway.discord.gg/?v=8&encoding=json"

__all__ = (
	"Gateway",
	"request",
)

def request(method, path, auth, data=None):
	base = "https://discord.com/api/v8"
	headers = {
		"Authorization": f"Bot {auth}"
	}
	if method == "POST":
		r = requests.post(base + path, json=data, headers=headers)
	elif method == "GET":
		r = requests.get(base + path, headers=headers)
	elif method == "DELETE":
		r = requests.delete(base + path, headers=headers)
	elif method == "PUT":
		r = requests.put(base + path, json=data, headers=headers)
	elif method == "PATCH":
		r = requests.patch(base + path, json=data, headers=headers)
	if r.status_code == 429:
		print("You are being rate limited!")
		try:
			time.sleep(json.loads(r.text)["retry_after"])
			print("running request again")
			request(method, path, auth, data)
		except:
			return
			# print(e)
	return r

class Gateway():
  # """Represents a Discord Gateway."""
	def __init__(self, json=False):
		self.json_v = json
		self.guilds = []

	async def start(self, loop):
		self.loop = loop
		self.connection = await websockets.connect(wssURL)
		response = await self.connection.recv()
		response = json.loads(response)
		print(response)
		self.interval = response["d"]["heartbeat_interval"]
		self.last_s = response["s"]
		data = {"op": 1, "d": self.last_s}
		await self.connection.send(json.dumps(data))
		identify_json = {
			"op": 2,
			"d": {
				"token": f"{discord.token}",
				"intents": 32767,
				"properties": {
					"$os": "linux",
					"$browser": "my_library",
					"$device": "my_library"
				}
			}
		}
		await self.connection.send(json.dumps(identify_json))
		print("done with start")
		return self.connection

	async def send(self, connection, message):
		"""Sends a message to the server"""
		await connection.send(json.dumps(message))

	async def quick_heartbeat(self, connection):
		"""send a single heartbeat with no interval"""
		try:
			data = {"op": 1, "d": self.last_s}
			await connection.send(json.dumps(data))
		except Exception as e:
			traceback.print_tb(e.__traceback__)
			print(str(e) + ' - heartbeat quick')

	async def heartbeat(self, connection):
		"""send a heartbeat every interval"""
		while True:
			try:
				data = {"op": 1, "d": self.last_s}
				await connection.send(json.dumps(data))
				await asyncio.sleep(self.interval / 1000)
			except Exception as e:
				traceback.print_tb(e.__traceback__)
				print(str(e) + ' - heartbeat')

	# [--- old listener ---]

	# async def listen(self, connection):  # sourcery no-metrics
	# 	"""Listens to events from the gateway.

	# 	Args:
	# 		connection (connection): The connection to the gateway.
	# 	"""
	# 	# TODO: Rewrite pretty much this whole thing :p
	# 	# TODO: I have to make a requests function for sure, I could split up the listeners into a separate function.
	# 	while True:
	# 		try:
	# 			message = await connection.recv()
	# 			message = json.loads(message)
	# 			pretty_message = json.dumps(message, indent=2)
	# 			op = message["op"]
	# 			print('Received message from server: \n' + str(pretty_message))
	# 			if op == 0:
	# 				self.last_s = message["s"]
	# 				title = message["t"]
	# 				# on_ready
	# 				if title == "READY":
	# 					if self.json_v:
	# 						with open("json/ready.json", "w", encoding="utf-8") as f:
	# 							json.dump(message, f, ensure_ascii=False, indent=2)
	# 					self.last_id = message["d"]["session_id"]
	# 					if message["d"]["user"]["bot"]:
	# 						self.user = discord.bot.Bot(message["d"]["user"])
	# 					else:
	# 						self.user = discord.user.User(message["d"]["user"])
	# 				# on_message
	# 				elif title == "MESSAGE_CREATE":
	# 					if self.json_v:
	# 						with open("json/message_create.json", "w", encoding="utf-8") as f:
	# 							json.dump(message, f, ensure_ascii=False, indent=2)
	# 				# on_interaction
	# 				elif title == "INTERACTION_CREATE":
	# 					if self.json_v:
	# 						with open("json/interaction_create.json", "w", encoding="utf-8") as f:
	# 							json.dump(message, f, ensure_ascii=False, indent=2)
	# 					inter = discord.interaction.Interaction(message["d"])
	# 					url = f"https://discord.com/api/v8/interactions/{inter.id}/{inter.token}/callback"
	# 					i_json = {
	# 						"type": 4,
	# 						"data": {
	# 							"content": "High Five!"
	# 						}
	# 					}
	# 					r = requests.post(url, json=i_json)
	# 				# on_guild_create
	# 				elif title == "GUILD_CREATE":
	# 					if self.json_v:
	# 						with open("json/guild_create.json", "w", encoding="utf-8") as f:
	# 							json.dump(message, f, ensure_ascii=False, indent=2)
	# 					guild = discord.guild.Guild(message["d"])
	# 					self.guilds.append(guild)
	# 			elif op == 1:
	# 				await self.quick_heartbeat(connection)
	# 			elif op == 9:
	# 				await self.send(connection, json.dumps(self.identify_json))
	# 			elif op == 10:
	# 				self.interval = message["d"]["heartbeat_interval"]
	# 		except Exception as e:
	# 			print(e)
	# 			print("- listen")
	# 			break

