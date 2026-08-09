from __future__ import annotations

import uuid
from pydantic import BaseModel, ConfigDict
from greatsky.db.orm.base import DatabaseEntry


class SessionModel(BaseModel):
    device_id: str
    model_config = ConfigDict(extra='forbid')


class Session(DatabaseEntry):
    def __init__(self, db_id: str, model: SessionModel | None = None):
        super().__init__(db_id=db_id, model=model)

    @classmethod
    def get_label(cls) -> str:
        return "Session"

    @classmethod
    def get_model_type(cls) -> type[BaseModel]:
        return SessionModel

    @classmethod
    def new(cls, model: SessionModel | None = None) -> Session:
        return Session(
            db_id=str(uuid.uuid4()),
            model=model,
        )