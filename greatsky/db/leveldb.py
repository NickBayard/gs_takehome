from threading import Lock

from greatsky.db.base import BaseKVDB

import plyvel


DEFAULT_LEVEL_DB_FILE = '/tmp/greatsky_db'


class LevelDB(BaseKVDB):
    _DB_LOCK = Lock()

    def __init__(self, db_file=DEFAULT_LEVEL_DB_FILE):
        if db_file is None:
            db_file = DEFAULT_LEVEL_DB_FILE
        self._DB_LOCK.acquire()
        self.db = plyvel.DB(db_file, create_if_missing=True)        

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
        self._DB_LOCK.release()

    def __setitem__(self, key: str, value: str) -> None:
        self.db.put(key.encode(), value.encode())

    def __getitem__(self, key: str) -> str | None:
        result = self.db.get(key.encode())
        return result.decode() if result is not None else None
    
    def __delitem__(self, key: str):
        self.db.delete(key.encode())