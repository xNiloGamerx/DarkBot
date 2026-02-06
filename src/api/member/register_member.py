from discord import Member
from supabase import Client

class RegisterMember:
    def __init__(self, connection: Client):
        self.connection = connection

    async def register_member(self, member: Member):
        # Logic to register the member in the database
        print(f"\n\nRegistering member: {member.name} (ID: {member.id})")
        binary_response = await self.connection.functions.invoke(
            "create-user",
            invoke_options={
                "body": {
                    "user_id": str(member.id), 
                    "username": member.name, 
                    "display_name": member.display_name, 
                    "joined_at": str(member.joined_at), 
                    "created_at": str(member.created_at), 
                    "guild_id": str(member.guild.id) 
                }
            }
        )
        response = binary_response.decode()
        print(f"Member registered. (Response: {response})")
        return response

    async def register_members(self, members: list[Member]):
        # Logic to register the member in the database
        print("\n\nRegistering multiple members...")
        binary_response = await self.connection.functions.invoke(
            "create-users",
            invoke_options={
                "body": [
                    {
                        "user_id": str(member.id), 
                        "username": member.name, 
                        "display_name": member.display_name, 
                        "joined_at": str(member.joined_at), 
                        "created_at": str(member.created_at), 
                        "guild_id": str(member.guild.id)
                    }
                    for member in members
                ]
            }
        )
        response = binary_response.decode()
        print(f"Members registered. (Response: {response})")
        return response
    
        