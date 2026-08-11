from greatsky.config import Config
from greatsky.db.leveldb import LevelDB
from greatsky.db.base import BaseKVDB

VALID_DB_MAP = {
    "leveldb": LevelDB
    # insert additional key-value data stores
    # implementing the BaseKVDB interface here.
}

_db_class_type = None


def get_db_class() -> type[BaseKVDB]:
    """
    The database class type is cached as a singleton so subsequent calls
    to this function (e.g. by each request handler thread) retrieve the
    same value.
    """
    global _db_class_type

    if _db_class_type is None:
        # The database type is specified in external config file
        # which allows for swapping of database concrete type
        # without code changes.
        config = Config.get()
        if config.database_type not in VALID_DB_MAP:
            raise ValueError(f"Invalid database type: {config.database_type}")
        _db_class_type = VALID_DB_MAP[config.database_type]
    return _db_class_type
