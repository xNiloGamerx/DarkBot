from supabase import FunctionsHttpError, create_client
import dotenv
import os

dotenv.load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

# response = supabase.functions.invoke(
#     "create-guild",
#     invoke_options={
#         "body": { "guild_id": "5", "name": "Darkunity", "created_at": "2025-12-14" }
#     }
# )

# response = supabase.functions.invoke(
#     "create-guilds",
#     invoke_options={
#         "body": [
#             { "guild_id": "839497766984089670", "name": "Darkunity", "created_at": "2025-12-14" },
#             { "guild_id": "819152506294763520", "name": "Test Server 2", "created_at": "2025-12-10" }
#         ]
#     }
# )

response = supabase.functions.invoke(
    "create-users",
    invoke_options={
        "body": [
            { "user_id": "838116158867374103", "username": "darktoad_", "display_name": "Darktoad", "joined_at": "2021-05-05", "created_at": "2021-05-01", "guild_id": "839497766984089670" },
            { "user_id": "838116158867374103", "username": "darktoad_", "display_name": "Darktoad", "joined_at": "2021-05-05", "created_at": "2021-05-01", "guild_id": "819152506294763520" },
            { "user_id": "752950649834176622", "username": "xxnilogamerxx", "display_name": "Nilo", "joined_at": "2022-08-04", "created_at": "2020-09-08", "guild_id": "839497766984089670" },
            { "user_id": "752950649834176622", "username": "xxnilogamerxx", "display_name": "Nilo", "joined_at": "2021-03-10", "created_at": "2020-09-08", "guild_id": "819152506294763520" },
        ]
    }
)

# response = supabase.functions.invoke(
#     "create-user",
#     invoke_options={
#         "body": { "user_id": "8", "username": "xxnilogamerxx", "display_name": "Nilo", "joined_at": "2021-03-10", "created_at": "2020-09-08", "guild_id": "819152506294763520" }
#     }
# )

print(response)
