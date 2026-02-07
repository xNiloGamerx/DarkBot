import json

from discord import Member
from supabase import Client

class DeleteMember:
    def __init__(self, connection: Client):
        self.connection = connection

    async def delete(self, member: Member = None, user_id: int = None) -> bool:
        # Logic to check if a channel is a counting channel in the database
        print(f"\n\nDeleting user for Member ID: {user_id or member.id}")
        binary_response = await self.connection.functions.invoke(
            "delete-user",
            invoke_options={
                "body": {
                    "user_id": str(user_id or member.id)
                }
            }
        )
        response = json.loads(binary_response.decode())
        print(f"User delete result: {response}")
        return response
