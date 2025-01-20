from typing import Any, Callable, Generic, Sequence, TypeVar
from psycopg import AsyncCursor
from shared.entity import Entity


T = TypeVar('T', bound=Entity)


class DbRepository(Generic[T]):
    def __init__(self, *, object_factory: Callable[..., T], fields_factory: Callable[[AsyncCursor[Any]], list[str]] = lambda cursor: [col.name for col in cursor.description] if cursor.description != None else []):
        self._object_factory = object_factory
        self._fields_factory = fields_factory

    def _row_factory(self, cursor: AsyncCursor[Any]) -> Callable[[Sequence[Any]], T]:
        fields = []

        if cursor.description != None:
            fields = self._fields_factory(cursor)

        def make_row(values: Sequence[Any]) -> T:
            return self._object_factory(dict(zip(fields, values)))

        return make_row
