import discord
import json
from munch import Munch, munchify

class Channel(Munch):
  def __init__(self, channel_obj):
    # Turns this class into a munch.
    super(Channel, self).__init__(channel_obj["d"])
  
  def __repr__(self):
    return json.dumps(self)

  def __str__(self):
    return f"Guild {self.name}, id {self.id}"