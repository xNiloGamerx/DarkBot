import json

from discord import Guild, Member
from supabase import Client

from api.connection import SupabaseConnection

class CountingGuild:
    def __init__(self, connection: Client):
        self.connection = connection

    def get(self, guild: Guild) -> bool:
        # Logic to check if a channel is a counting channel in the database
        print(f"\n\nGetting counting guild for Guild ID: {guild.id}")
        response = self.connection.functions.invoke(
            "get-counting-guild",
            invoke_options={
                "body": {
                    "guild_id": str(guild.id)
                }
            }
        )
        print(f"Counting guild get result: {response}")
        return json.loads(response.decode())[0]
