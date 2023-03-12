import asyncio
from db_commands import Database
db = Database()


async def run_test():
    await db.create()
    await db.delete_all_users()
    print("Users have been deleted")
asyncio.get_event_loop().run_until_complete(run_test())

