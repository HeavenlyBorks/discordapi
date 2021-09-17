import json

class Guild():
  def __init__(self, guild):
    self.guild = guild["d"]

    # get guild channels
    for channel in self.guild["channels"]:
      pass

    # guild name
    self.name = self.guild["name"]
    # guild id
    self.id = self.guild["id"]
  
  def __repr__(self):
    return json.dumps(self.guild)

  def __str__(self):
    return f"Guild {self.name}, id {self.id}"