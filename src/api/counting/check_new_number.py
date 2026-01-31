import json

from discord import TextChannel, Guild
from supabase import Client

from api.connection import SupabaseConnection

class CheckNewNumber:
    def __init__(self, connection: Client):
        self.connection = connection

    def check_new_number(self, guild: Guild, user_counted: TextChannel, counted_number: int) -> bool:
        # Logic to check if a channel is a counting channel in the database
        print(f"\n\nChecking if user {user_counted.name} ({user_counted.id}) that counted number {counted_number} for Guild {guild.name} ({guild.id}) is right...")
        response = self.connection.functions.invoke(
            "new-number",
            invoke_options={
                "body": {
                    "channel_id": str(user_counted.id),
                    "guild_id": str(guild.id),
                    "counted_number": counted_number
                }
            }
        )
        print(f"Response from new-number function: {response}")
        return json.loads(response.decode()).get("result", False)
