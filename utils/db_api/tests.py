from db_sqlalchemy import Database
import asyncio

DATABASE_URL = 'postgresql+asyncpg://postgres:khamid007@localhost:5432/db_medication'


async def test_db():
    db = Database(DATABASE_URL)
    users = await db.select_all_users()
    for user in users:
        print(user)

if __name__ == '__main__':
    asyncio.run(test_db())