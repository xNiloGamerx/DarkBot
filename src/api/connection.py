from supabase import acreate_client, AsyncClient
import dotenv
import os

dotenv.load_dotenv()

class SupabaseConnection:
    def __init__(self):
        self.base_url = os.getenv("SUPABASE_URL")
        self.service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    def _create_connection(self):
        supabase: AsyncClient = acreate_client(
            self.base_url, 
            self.service_role_key
        )
        return supabase