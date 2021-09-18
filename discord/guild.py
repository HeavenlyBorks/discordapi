from munch import Munch, munchify
from discord.channel import Channel
import json

class Guild(Munch):
  def __init__(self, guild):
    super(Guild, self).__init__(guild["d"])
  
  def __repr__(self):
    return json.dumps(self)

  def __str__(self):
    return f"Guild {self.name}, id {self.id}"