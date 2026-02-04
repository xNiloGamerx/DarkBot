import json

from discord import TextChannel, Guild
from supabase import Client

from api.connection import SupabaseConnection

class WrongNumber:
    def __init__(self, connection: Client):
        self.connection = connection

    async def run(self, counting_guild_id: int) -> bool:
        # Logic to check if a channel is a counting channel in the database
        print(f"\n\nRun Wrong Number routine, set last_counted_number to checkpoint and last_counted_user_id to none and checkpoint to 0 for Counting Guild ID: {counting_guild_id}...")
        response = await self.connection.functions.invoke(
            "wrong-number",
            invoke_options={
                "body": {
                    "id": counting_guild_id
                }
            }
        )
        print(f"Wrong number result: {response}")
        return json.loads(response.decode())
