from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Any, Self
from greatsky.db import BaseKVDB
from pydantic import BaseModel, Field

KEY_DELIMITER: str = ':::'

class DatabaseEntry(ABC, BaseModel):
    db_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    model: BaseModel | Any = None

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
        return f'{cls.get_label()}{KEY_DELIMITER}{key}'

    @classmethod
    def strip_key(cls, key: str):
        return KEY_DELIMITER.split(key)[-1]

    @classmethod
    def deserialize_model(cls, serialized: str) -> BaseModel:
        return cls.get_model_type().model_validate_json(serialized)

    def update(self, db: BaseKVDB):
        """
        Serialize object and write to database.
        This can be used to both create new entries as well
        as update existing ones.
        """
        db[self.make_key(self.db_id)] = self.model.model_dump_json()

    @classmethod
    def get(cls, key: str, db: BaseKVDB) -> Self:
        """
        Read object from database and deserialize
        """
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
    def get_all(cls, db: BaseKVDB) -> list[Self]:
        """
        Read all objects of this type from database and return
        a list of deserialized objects
        """
        entries = db.read_all(prefix=f'{cls.get_label()}:')
        return [
            cls(
                db_id=cls.strip_key(k),
                model=cls.deserialize_model(v)
            ) for k, v in entries.items()
        ]

    @classmethod
    def delete(cls, key: str, db: BaseKVDB) -> None:
        """
        Remove an entry from the database
        """
        full_key = cls.make_key(key)
        del db[full_key]