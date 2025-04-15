from infra.database import database


async def get_db_connection():
    async with database.get_connection() as connection:
        yield connection
