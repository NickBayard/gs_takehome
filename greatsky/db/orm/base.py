from __future__ import annotations

from abc import ABC, abstractmethod
from greatsky.db import BaseKVDB
from pydantic import BaseModel


class DatabaseEntry(ABC):
    def __init__(self, db_id: str, model: BaseModel):
        self._id = db_id
        self.model = model

    @classmethod
    @abstractmethod
    def get_label(cls) -> str:
        pass
    
    @classmethod
    @abstractmethod
    def get_model_type(cls) -> type[BaseModel]:
        pass

    @classmethod
    def make_key(cls, key: str):
        return f'{cls.get_label()}:{key}'

    @classmethod
    def strip_key(cls, key: str):
        return ':'.split(key)[-1]

    @classmethod
    def deserialize_model(cls, serialized: str) -> BaseModel:
        return cls.get_model_type().model_validate_json(serialized)

    def update(self, db: BaseKVDB):
        db[self.make_key(self._id)] = self.model.model_dump_json()

    @classmethod
    def read(cls, key: str, db: BaseKVDB) -> DatabaseEntry:
        full_key = cls.make_key(key)
        value = db[full_key]
        if value is None:
            raise KeyError(f'{cls.get_label()} {key} not found')
        # Convert value to Session
        return cls(
            db_id=key,
            model=cls.deserialize_model(value),
        )

    @classmethod
    def read_all(cls, db: BaseKVDB) -> list[DatabaseEntry]:
        entries = db.read_all(prefix=f'{cls.get_label()}:')
        return [
            cls(
                db_id=cls.strip_key(k),
                model=cls.deserialize_model(v)
            ) for k, v in entries.items()
        ]

    @classmethod
    def delete(cls, key: str, db: BaseKVDB) -> None:
        full_key = cls.make_key(key)
        del db[full_key]