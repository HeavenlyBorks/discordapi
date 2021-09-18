import discord
from munch import Munch
import json

class Guild(Munch):
  def __init__(self, guild):
    super(Guild, self).__init__(guild)
    self.channels = [discord.channel.Channel(channel) for channel in self.channels]
  
  def __repr__(self):
    return json.dumps(self)

  def __str__(self):
    return f"Guild {self.name}, id {self.id}"