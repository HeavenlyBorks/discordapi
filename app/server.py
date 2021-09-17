import json

class Server():
  def __init__(self, guild):
    self.guild_object = guild["d"]

    self.name = self.guild_object["name"]
  
  def __repr__(self):
    return json.dumps(self.guild_object)

  def __str__(self):
    return 