import discord
import json

__all__ = (
    "TextChannel",
    "get_channel",
)

class TextChannel():
  def __init__(self, c):
    self.id = c["id"]
    self.guild_id = c.get("guild_id", None)
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

  def send(self, content=None, tts=None, file=None, embeds=None, mentions=None, reference=None, components=None, stickers=None):
      payload = discord.make_payload(content, tts, file, embeds, mentions, reference, components, stickers)
      r = discord.request("POST", f"/channels/{self.id}/messages", discord.token, data=payload)
  
  def __repr__(self):
    return json.dumps(self)

  def __str__(self):
    return f"Guild {self.name}, id {self.id}"

def get_channel(id):
    r = discord.request("GET", f"/channels/{id}", discord.token)
    return discord.TextChannel(json.loads(r.text))