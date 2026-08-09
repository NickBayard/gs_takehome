from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from greatsky.db import BaseKVDB
from greatsky.db.orm.base import DatabaseEntry
from pydantic import BaseModel, ConfigDict


class DeviceModel(BaseModel):
    active_session_id: str
    model_config = ConfigDict(extra='forbid')


class Device(DatabaseEntry):
    @classmethod
    def get_label(cls) -> str:
        return "Device"

    @classmethod
    def get_model_type(cls) -> type[BaseModel]:
        return DeviceModel