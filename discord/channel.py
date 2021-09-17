import discord

class Channel():
  def __init__(self, channel):
    self.channel = channel["d"]

    # channel type
    self.type = self.channel["type"]
    # channel name
    self.name = self.channel["name"]