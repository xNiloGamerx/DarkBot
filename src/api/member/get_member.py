import json

from discord import Member
from supabase import Client

class GetMember:
    def __init__(self, connection: Client):
        self.connection = connection

    async def get(self, member: Member = None, user_id: int = None) -> bool:
        # Logic to check if a channel is a counting channel in the database
        print(f"\n\nGetting user for Member ID: {user_id or member.id}")
        binary_response = await self.connection.functions.invoke(
            "get-user",
            invoke_options={
                "body": {
                    "user_id": str(user_id or member.id)
                }
            }
        )
        response = json.loads(binary_response.decode())
        print(f"User get result: {response}")
        if len(response) <= 0:
            return False
        else:
            return response[0]
        
    async def get_by_id(self, id: int):
        # Logic to check if a channel is a counting channel in the database
        print(f"\n\nGetting user for ID: {id}")
        binary_response = await self.connection.functions.invoke(
            "get-user-by-id",
            invoke_options={
                "body": {
                    "id": id
                }
            }
        )
        response = json.loads(binary_response.decode())
        print(f"User get result: {response}")
        if len(response) <= 0:
            return False
        else:
            return response[0]
