from supabase import create_client
import dotenv
import os

dotenv.load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("DATABASE_ANON_KEY"))

response = supabase.functions.invoke(
    "hello-world",
    invoke_options={
        "body": {"name": "Niklas"}
    }
)

print(response)
