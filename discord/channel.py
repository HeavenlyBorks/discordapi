import discord
import json

__all__ = (
    "TextChannel",
)

class TextChannel():
  def __init__(self, c):
    self.id = c["id"]
    self.guild_id = c["guild_id"] or None
    self.type = c["type"]
    self.postition = c["position"] or None
    self.permission_overwrites = c["permission_overwrites"] or None
    self.name = c["name"]
    self.topic = c["topic"] or None
    self.nsfw = c["nsfw"] or False
    self.last_message_id = c["last_message_id"] or None
    self.rate_limit = c["rate_limit_per_user"] or 0
    self.parent_id = c["parent_id"] or None
    self.last_pin_timestamp = c["last_pin_timestamp"] or None

  def send(self, message):
      # TODO: make a message class
      pass
  
  def __repr__(self):
    return json.dumps(self)

  def __str__(self):
    return f"Guild {self.name}, id {self.id}"