from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_user(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users_telegramuser(
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        registered_time varchar(50) NOT NULL
         );
         """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id, registered_time=None, registered_date=None):
        sql = "INSERT INTO users_telegramuser (full_name, username, telegram_id, registered_time) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, full_name, username, telegram_id, registered_time, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users_telegramuser"
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                results = await conn.fetch(sql)
                return [dict(r) for r in results]

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users_telegramuser"
        return await self.execute(sql, fetchval=True)

    async def delete_all_users(self):
        await self.execute("DELETE FROM users_telegramuser WHERE TRUE", execute=True)

    async def check_user(self, telegram_id):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                sql = "SELECT COUNT(*) FROM users_telegramuser WHERE telegram_id = $1"
                result = await conn.fetchval(sql, telegram_id)
                return result > 0

    async def users_prescriptions(self):
        sql = """CREATE TABLE IF NOT EXISTS prescriptions (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        medication_name VARCHAR(255) NOT NULL,
        dosage VARCHAR(255) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users_telegramuser(user_id)
        );
        """
        await self.execute(sql, execute=True)
