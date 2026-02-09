import json
from discord import Guild, Member

from supabase import Client

class CheckIfMemberExists:
    def __init__(self, connection: Client) -> bool:
        self.connection = connection

    async def check_if_member_exists(self, member: Member, guild: Guild):
        print(f"\n\nCheck if member exists for member: {member.name} (ID: {member.id})")
        binary_response = await self.connection.functions.invoke(
            "check-if-user-exists",
            invoke_options={
                "body": {
                    "user_id": str(member.id),
                    "guild_id": str(guild.id)
                }
            }
        )
        response = binary_response.decode()
        print(f"Check if member exists result: {response}")
        if response:
            return json.loads(response)["result"]
        else:
            return False
