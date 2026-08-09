from __future__ import annotations
from abc import ABC, abstractmethod


class BaseKVDB(ABC):

    def __enter__(self) -> BaseKVDB:
        return self

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    @abstractmethod
    def __setitem__(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def __getitem__(self, key: str) -> str:
        pass
    
    @abstractmethod
    def __delitem__(self, key: str):
        pass

    @abstractmethod
    def read_all(self, prefix: str) -> dict[str, str]:
        pass