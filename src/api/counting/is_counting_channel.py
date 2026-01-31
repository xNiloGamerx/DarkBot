import json

from discord import TextChannel, Guild
from supabase import Client

from api.connection import SupabaseConnection

class IsCountingChannel:
    def __init__(self, connection: Client):
        self.connection = connection

    def is_counting_channel(self, guild: Guild, channel: TextChannel) -> bool:
        # Logic to check if a channel is a counting channel in the database
        print(f"\n\nChecking if channel {channel.id} is a counting channel for Guild ID: {guild.id}...")
        response = self.connection.functions.invoke(
            "is-counting-channel",
            invoke_options={
                "body": {
                    "channel_id": str(channel.id),
                    "guild_id": str(guild.id)
                }
            }
        )
        print(f"Counting channel check result: {response}")
        return json.loads(response.decode()).get("result", False)
