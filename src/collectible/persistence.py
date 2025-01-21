from psycopg import Column
from collectible.model import Collectible
from shared import db_pool
from shared.db_repository import DbRepository


class CollectiblesPersistence(DbRepository[Collectible]):
    def __init__(self):
        def object_factory(dict):
            return Collectible(**dict)

        def fields_factory(columns: list[Column]):
            return [col.name if col.name != "collectible_id" else "id" for col in columns]

        super().__init__(object_factory=object_factory, fields_factory=fields_factory)

    async def test(self):
        async with db_pool.cursor(self._row_factory) as cursor:
            await cursor.execute("SELECT * FROM collectible")
            return await cursor.fetchall()
