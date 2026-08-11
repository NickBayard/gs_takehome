from fastapi import (
    APIRouter,
    Response,
    status,
)
from greatsky.db import get_db_class
from greatsky.db.orm import (
    Device,
    DeviceModel,
)
from greatsky.utils import Tag

router = APIRouter()

# get_db_class allows us to swap out another key-value data store
# provided that a facade has been created to follow the BaseKVDB
# interface.  This class uses the YAML config file to determine
# the database class type.
DB_TYPE = get_db_class()


@router.post(
    "/devices/",
    tags=[Tag.devices],
    status_code=status.HTTP_201_CREATED,
)
def create_device(model: DeviceModel):
    """
    Create a new device instance.
    """
    with DB_TYPE() as db:
        device = Device(
            model=model,
        )
        device.update(db)
    return device.model_dump_json()


@router.get(
    "/devices/{device_id}",
    tags=[Tag.devices],
    status_code=status.HTTP_200_OK,
)
def get_device(device_id: str, response: Response):
    """
    Get a specific device.
    """
    with DB_TYPE() as db:
        try:
            device = Device.get(device_id, db)
        except KeyError:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": f"Device not found: {device_id}"}

    return device.model_dump_json()


@router.get(
    "/devices/",
    tags=[Tag.devices],
    status_code=status.HTTP_200_OK,
)
def get_all_devices():
    """
    List all devices.
    """
    with DB_TYPE() as db:
        devices = Device.get_all(db)

    return {"devices": [device.model_dump_json() for device in devices]}


@router.patch(
    "/devices/{device_id}",
    tags=[Tag.devices],
    status_code=status.HTTP_200_OK,
)
def update_device(device_id: str, model: DeviceModel, response: Response):
    """
    Update a specific device shape with some parameters.
    """
    with DB_TYPE() as db:
        try:
            device = Device.get(device_id, db)
        except KeyError:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": f"Device not found: {device_id}"}

        # Replace the model wholesale
        device.model = model
        device.update(db)

    return device.model_dump_json()
