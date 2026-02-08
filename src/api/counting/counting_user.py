import json

from discord import Guild, Member
from supabase import Client

from api.connection import SupabaseConnection

class CountingUser:
    def __init__(self, connection: Client):
        self.connection = connection

    async def get_or_create(self, guild: Guild, member: Member) -> bool:
        # Logic to check if a channel is a counting channel in the database
        print(f"\n\nGetting or creating counting user for Member ID: {member.id}, Guild ID: {guild.id}")
        binary_response = await self.connection.functions.invoke(
            "get-or-create-counting-user",
            invoke_options={
                "body": {
                    "user_id": str(member.id),
                    "guild_id": str(guild.id)
                }
            }
        )
        response = json.loads(binary_response.decode())
        print(f"User Counting get or create result: {response}")
        if response:
            return response[0]
        else:
            return None
    
    async def update(self, id: int, count_total: int | None = None, count_errors: int | None = None, avg_count_reaction_time: int | None = None, count_points: int | None = None, last_counted_at: str | None = None):
        if not id:
            raise ValueError(f"{__file__}: ID is required to update Counting User.")

        print(f"\n\nUpdating counting user for Counting User ID: {id}")
        response = await self.connection.functions.invoke(
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

    async def delete(self, guild: Guild, member: Member) -> bool:
        # Logic to check if a channel is a counting channel in the database
        print(f"\n\nDeleting counting user for Member ID: {member.id}, Guild ID: {guild.id}")
        response = await self.connection.functions.invoke(
            "delete-counting-user",
            invoke_options={
                "body": {
                    "user_id": str(member.id),
                    "guild_id": str(guild.id)
                }
            }
        )
        print(f"Delete Counting User result: {response}")
        return json.loads(response.decode())
