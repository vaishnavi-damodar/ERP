import asyncio
from app.core.database import db

async def get_users():
    try:
        result = db.query('users').select('*').limit(5).execute()
        print(result.data)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(get_users())
