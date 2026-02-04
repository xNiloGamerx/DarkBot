from discord import TextChannel

from api.connection import SupabaseConnection

class RegisterChannel:
    def __init__(self, connection: SupabaseConnection):
        self.connection = connection

    async def register_channel(self, channel: TextChannel):
        # Logic to register a channel in the database
        print(f"\n\nRegistering channel: {channel.name} (ID: {channel.id})")
        response = await self.connection.functions.invoke(
            "create-channel",
            invoke_options={
                "body": {
                    "channel_id": str(channel.id),
                    "name": str(channel.name),
                    "created_at": str(channel.created_at)
                }
            }
        )
        print(f"Channel registered. (Response: {response})")
        return response    
        