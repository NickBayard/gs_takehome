from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from greatsky.db import BaseKVDB
from greatsky.db.orm.base import DatabaseEntry
from pydantic import BaseModel, ConfigDict


class DeviceModel(BaseModel):
    pass


class Device(DatabaseEntry):
    pass