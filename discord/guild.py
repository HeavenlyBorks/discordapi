import discord
import json

__all__ = (
    "Guild",
    "get_guild",
)

class Guild:
  def __init__(self, g):
      self.id = g.get("id")
      self.name = g.get("name")
      self.icon = g.get("icon", None)
      self.icon_hash = g.get("icon_hash", None)
      self.splash = g.get("splash", None)
      self.discovery_splash = g.get("discovery_splash", None)
      self.owner = g.get("owner", False)
      self.owner_id = g.get("owner_id")
      self.permissions = g.get("permissions", None)
      self.afk_channel_id = g.get("afk_channel_id", None)
      self.afk_timeout = g.get("afk_timeout")
      self.widget_enabled = g.get("widget_enabled", None)
      self.widget_channel_id = g.get("widget_channel_id", None)
      self.verification_level = g.get("verification_level")
      self.default_message_notifications = g.get("default_message_notifications")
      self.explicit_content_filter = g.get("explicit_content_filter")
      # TODO: make role object
      self.roles = g.get("roles")
      # TODO: make emoji object
      self.emojis = g.get("emojis")
      self.features = g.get("features")
      self.mfa_level = g.get("mfa_level")
      self.application_id = g.get("application_id", None)
      self.system_channel_id = g.get("system_channel_id", None)
      self.system_channel_flags = g.get("system_channel_flags", None)
      self.rules_channel_id = g.get("rules_channel_id", None)
      self.joined_at = g.get("joined_at", None)
      self.large = g.get("large", False)
      self.unavailable = g.get("unavailable", False)
      self.member_count = g.get("member_count", None)
      self.voice_states = g.get("voice_states", None)
      # TODO: make guild member object
      self.members = g.get("members", None)
      self.channels = g.get("channels", None)
      self.threads = g.get("threads", None)
      self.presences = g.get("presences", None)
      self.max_presences = g.get("max_presences", None)
      self.max_members = g.get("max_members", None)
      self.vanity_url_code = g.get("vanity_url_code", None)
      self.description = g.get("description", None)
      self.banner = g.get("banner", None)
      self.premium_tier = g.get("premium_tier")
      self.premium_subcription_count = g.get("premium_subcription_count", 0)
      self.preferred_locale = g.get("preferred_locale")
      self.public_updates_channel_id = g.get("public_updates_channel_id", None)
      self.max_video_channel_users = g.get("max_video_channel_users", None)
      self.approximate_member_count = g.get("approximate_member_count", None)
      self.approximate_presence_count = g.get("approximate_presence_count", None)
      self.welcome_screen = g.get("welcome_screen", None)
      self.nsfw_level = g.get("nsfw_level")
      # TODO: look at welcome screens
      self.stage_instances = g.get("stage_instances", None)
      # TODO: make stickers object
      self.stickers = g.get("stickers", None)
  
  def __repr__(self):
    return json.dumps(self)

  def __str__(self):
    return f"Guild {self.name}, id {self.id}"

async def get_guild(id):
    r = discord.request("GET", f"/guilds/{id}", discord.token)
    return discord.Guild(json.loads(r.text))