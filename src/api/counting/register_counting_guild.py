from discord import TextChannel, Guild

from api.connection import SupabaseConnection

class RegisterCountingGuild:
    def __init__(self, connection: SupabaseConnection):
        self.connection = connection

    async def register_counting_guild(self, guild: Guild, channel: TextChannel):
        # Logic to register a counting guild in the database
        print(f"\n\nRegistering counting guild for Guild ID: {guild.id}, Channel ID: {channel.id}...")
        response = await self.connection.functions.invoke(
            "create-counting-guild",
            invoke_options={
                "body": {
                    "channel_id": str(channel.id),
                    "guild_id": str(guild.id)
                }
            }
        )
        print(f"Counting guild registered. (Response: {response})")
        return response    
        