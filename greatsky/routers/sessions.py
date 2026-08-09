from fastapi import APIRouter
from greatsky.db import get_db_class
from greatsky.routers.tags import Tag

router = APIRouter()

# get_db_class allows us to swap out another key-value data store
# provided that a facade has been created to follow the BaseKVDB
# interface.  This class uses the YAML config file to determine
# the database class type.
DB_TYPE = get_db_class()

@router.post("/devices/{device_id}/sessions/", tags=[Tag.sessions])
def create_device_session(device_id: str):
    with DB_TYPE() as db:
        return {k:v for k,v in db.db}


@router.post("/devices/sessions/", tags=[Tag.sessions])
def create_session():
    with DB_TYPE() as db:
        return {k:v for k,v in db.db}