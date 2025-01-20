from collectible.model import Collectible
from shared import db_pool
from shared.db_repository import DbRepository


class CollectiblesPersistence(DbRepository[Collectible]):
    def __init__(self):
        super().__init__(object_factory=lambda dict: Collectible(**dict), fields_factory=lambda cursor: [col.name if col.name !=
                                                                                                         "collectible_id" else "id" for col in cursor.description] if cursor.description != None else [])

    async def test(self):
        async with db_pool.cursor(self._row_factory) as cursor:
            await cursor.execute("SELECT * FROM collectible")
            return await cursor.fetchall()
