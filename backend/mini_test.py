import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

print(f"URL: {url}")
print(f"Key starts with: {key[:10] if key else 'None'}...")

try:
    client = create_client(url, key)
    print("Client created successfully")
except Exception as e:
    import traceback
    traceback.print_exc()
