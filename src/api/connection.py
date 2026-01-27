from supabase import FunctionsHttpError, create_client
import dotenv
import os

dotenv.load_dotenv()

class SupabaseConnection:
    def __init__(self):
        self.base_url = os.getenv("SUPABASE_URL")
        self.service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    def _create_connection(self):
        supabase = create_client(
            self.base_url, 
            self.service_role_key
        )
        return supabase