from threading import Lock

from greatsky.db.base import BaseKVDB

import plyvel

DEFAULT_LEVEL_DB_FILE = "/tmp/greatsky_db"


class LevelDB(BaseKVDB):
    # Each request handler gets it's own instance of LevelDB
    # This class attribute lock is used to ensure that only one
    # can access the DB at a time.  This service currently only
    # supports running as a single process (no gunicorn), so we
    # don't have to worry about locking across processes.  For that
    # LevelDB would not be appropriate and a standalone server data
    # store should be used.
    lock = Lock()

    def __init__(self, db_file=DEFAULT_LEVEL_DB_FILE):
        if db_file is None:
            db_file = DEFAULT_LEVEL_DB_FILE
        self.db = plyvel.DB(db_file, create_if_missing=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def __setitem__(self, key: str, value: str) -> None:
        with self.lock:
            self.db.put(key.encode(), value.encode())

    def __getitem__(self, key: str) -> str | None:
        with self.lock:
            result = self.db.get(key.encode())
        return result.decode() if result is not None else None

    def __delitem__(self, key: str):
        with self.lock:
            self.db.delete(key.encode())

    def read_all(self, prefix: str) -> dict[str, str]:
        with self.lock:
            result = {k: v for k, v in self.db.iterator(prefix=prefix.encode())}
        return result
