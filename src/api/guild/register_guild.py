from discord import Guild
from supabase import Client

class RegisterGuild:
    def __init__(self, connection: Client):
        self.connection = connection

    async def register_guild(self, guild: Guild):
        # Logic to register the guild in the database
        print(f"\n\nRegistering guild: {guild.name} (ID: {guild.id})")
        binary_response = await self.connection.functions.invoke(
            "create-guild",
            invoke_options={
                "body": { "guild_id": str(guild.id), "name": guild.name, "created_at": str(guild.created_at) }
            }
        )
        response = binary_response.decode()
        print(f"Guild registered. (Response: {response})")
        return response

    async def register_guilds(self, guilds: list[Guild]):
        # Logic to register the guild in the database
        print("\n\nRegistering mutliple guilds...")
        print(f"Guilds to register: {[guild.name for guild in guilds]}")
        binary_response = await self.connection.functions.invoke(
            "create-guilds",
            invoke_options={
                "body": [
                    { "guild_id": str(guild.id), "name": guild.name, "created_at": str(guild.created_at) }
                    for guild in guilds
                ]
            }
        )
        response = binary_response.decode()
        print(f"Guilds registered. (Response: {response})")
        return response
    
        