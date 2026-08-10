from __future__ import annotations

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)
from greatsky.db.orm.base import DatabaseEntry


class UserModel(BaseModel):
    email: str  # TODO No validation
    hashed_password: str
    permissions: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra='forbid')


class User(DatabaseEntry):
    @classmethod
    def get_label(cls) -> str:
        return "User"

    @classmethod
    def get_model_type(cls) -> type[BaseModel]:
        return UserModel