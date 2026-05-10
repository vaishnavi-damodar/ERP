import asyncio
import sys
from app.core.database import db

async def test_connection():
    try:
        # Try fetching a row from the departments table to test connection
        result = db.query("departments").select("*").limit(1).execute()
        print("SUCCESS! Connected to Supabase.")
        print(f"Departments table check: {result.data}")
        sys.exit(0)
    except Exception as e:
        import traceback
        print(f"FAILED to connect or query: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_connection())
