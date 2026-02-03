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

    def update(self, id: int, last_counted_number: int | None = None, last_counted_user_id: int | None = None, count_checkpoint: int | None = None, count_points: int | None = None, last_counted_at: str | None = None):
        if not id:
            raise ValueError(f"{__file__}: ID is required to update Counting Guild.")

        print(f"\n\nUpdating counting guild for Counting Guild ID: {id}")
        response = self.connection.functions.invoke(
            "update-counting-guild",
            invoke_options={
                "body": {
                    "id": id,
                    "last_counted_number": last_counted_number,
                    "last_counted_user_id": last_counted_user_id,
                    "count_checkpoint": count_checkpoint,
                    "count_points": count_points,
                    "last_counted_at": last_counted_at
                }
            }
        )
        print(f"Guild Counting update result: {response}")
        return json.loads(response.decode())
