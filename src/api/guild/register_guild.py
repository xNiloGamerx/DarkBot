from discord import Guild

from api.connection import SupabaseConnection

class RegisterGuild:
    def __init__(self, connection: SupabaseConnection):
        self.connection = connection

    def register_guild(self, guild: Guild):
        # Logic to register the guild in the database
        print(f"\n\nRegistering guild: {guild.name} (ID: {guild.id})")
        response = self.connection.functions.invoke(
            "create-guild",
            invoke_options={
                "body": { "guild_id": str(guild.id), "name": guild.name, "created_at": str(guild.created_at) }
            }
        )
        print(f"Guild registered. (Response: {response})")
        return response

    def register_guilds(self, guilds: list[Guild]):
        # Logic to register the guild in the database
        print("\n\nRegistering mutliple guilds...")
        print(f"Guilds to register: {[guild.name for guild in guilds]}")
        response = self.connection.functions.invoke(
            "create-guilds",
            invoke_options={
                "body": [
                    { "guild_id": str(guild.id), "name": guild.name, "created_at": str(guild.created_at) }
                    for guild in guilds
                ]
            }
        )
        print(f"Guilds registered. (Response: {response})")
        return response
    
        