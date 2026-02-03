import json

from discord import Guild, Member
from supabase import Client

from api.connection import SupabaseConnection

class CountingUser:
    def __init__(self, connection: Client):
        self.connection = connection

    def get_or_create(self, guild: Guild, member: Member) -> bool:
        # Logic to check if a channel is a counting channel in the database
        print(f"\n\nGetting or creating counting user for Member ID: {member.id}, Guild ID: {guild.id}")
        response = self.connection.functions.invoke(
            "get-or-create-counting-user",
            invoke_options={
                "body": {
                    "user_id": str(member.id),
                    "guild_id": str(guild.id)
                }
            }
        )
        print(f"User Counting get or create result: {response}")
        return json.loads(response.decode())[0]
    
    def update(self, id: int, count_total: int | None = None, count_errors: int | None = None, avg_count_reaction_time: int | None = None, count_points: int | None = None, last_counted_at: str | None = None):
        if not id:
            raise ValueError(f"{__file__}: ID is required to update Counting User.")

        print(f"\n\nUpdating counting user for Counting User ID: {id}")
        response = self.connection.functions.invoke(
            "update-counting-user",
            invoke_options={
                "body": {
                    "id": id,
                    "count_total": count_total,
                    "count_errors": count_errors,
                    "avg_count_reaction_time": avg_count_reaction_time,
                    "count_points": count_points,
                    "last_counted_at": last_counted_at
                }
            }
        )
        print(f"User Counting update result: {response}")
        return json.loads(response.decode())
