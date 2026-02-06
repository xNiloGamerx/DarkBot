import json
from supabase import Client

class Shop:
    def __init__(self, connection: Client):
        self.connection = connection

    async def buy_checkpoint(self, counting_guild_id, price) -> bool:
        try:
            print(f"\n\nBuying Checkpoint for counting_guild_id: {counting_guild_id} and price: {price}")
            binary_response = await self.connection.functions.invoke(
                "buy-checkpoint",
                invoke_options={
                    "body": {
                        "id": counting_guild_id,
                        "price": price
                    }
                }
            )
            response = binary_response.decode()
            print(f"Buy Checkpoint result: {response}")
            if response:
                return json.loads(response)
            else:
                return False
        except Exception as e:
            print(f"Error in shop api buy_checkpoint:  {e}")