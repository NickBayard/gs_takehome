from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from greatsky.db.orm.base import DatabaseEntry


class SessionModel(BaseModel):
    device_id: str
    active: bool
    model_config = ConfigDict(extra="forbid")


class Session(DatabaseEntry):
    @classmethod
    def get_label(cls) -> str:
        return "Session"

    @classmethod
    def get_model_type(cls) -> type[BaseModel]:
        return SessionModel
