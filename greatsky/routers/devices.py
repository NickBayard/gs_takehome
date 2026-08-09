from fastapi import APIRouter
from greatsky.db import get_db_class

router = APIRouter()

# get_db_class allows us to swap out another key-value data store
# provided that a facade has been created to follow the BaseKVDB
# interface.  This class uses the YAML config file to determine
# the database class type.
DB_TYPE = get_db_class()

@router.post("/devices/", tags=['devices'])
def create_device():
    with DB_TYPE() as db:
        return {k:v for k,v in db.db}