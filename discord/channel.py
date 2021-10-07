import discord
import json
import asyncio
import nest_asyncio
nest_asyncio.apply()

__all__ = (
    "TextChannel",
    "get_channel",
)

class TextChannel:
  def __init__(self, c):
    self.id = c["id"]
    self.guild_id = c.get("guild_id", None)
    self.guild = discord.main_loop.run_until_complete(discord.get_guild(self.guild_id)) if self.guild_id else None
    self.type = c["type"] 
    self.postition = c.get("position", None)
    self.permission_overwrites = c.get("permission_overwrites", None)
    self.name = c["name"]
    self.topic = c.get("topic", None)
    self.nsfw = c.get("nsfw", None)
    self.last_message_id = c.get("last_message_id", None)
    self.rate_limit = c.get("rate_limit_per_user", None)
    self.parent_id = c.get("parent_id", None)
    self.last_pin_timestamp = c.get("last_pin_timestamp", None)

  async def send(self, content=None, tts=None, file=None, embeds=None, mentions=None, reference=None, components=None, stickers=None):
      payload = discord.make_message_payload(content, tts, file, embeds, mentions, reference, components, stickers)
      r = discord.request("POST", f"/channels/{self.id}/messages", discord.token, data=payload)
      r = json.loads(r.text)
      r["guild_id"] = self.guild_id
      r["channel_id"] = self.id
      return discord.Message(r)
  
  def __repr__(self):
    return json.dumps(self)

  def __str__(self):
    return f"Guild {self.name}, id {self.id}"

  async def get_message(self, i):
      r = discord.request("GET", f"/channels/{self.id}/messages/{i}", discord.token)
      return discord.Message(json.loads(r.text))

async def get_channel(id):
    r = discord.request("GET", f"/channels/{id}", discord.token)
    return discord.TextChannel(json.loads(r.text))