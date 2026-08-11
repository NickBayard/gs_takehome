from fastapi import (
    APIRouter,
    Response,
    status,
)
from greatsky.db import get_db_class
from greatsky.db.orm import Device
from greatsky.drivers.base import EdgeDriver
from greatsky.routers.models import (
    SetEdgesWeightsRequest,
    SetEdgesWeightsResponse,
)
from greatsky.utils import (
    validate_session_and_device,
    SessionDeviceError,
    Tag,
)

router = APIRouter()

# get_db_class allows us to swap out another key-value data store
# provided that a facade has been created to follow the BaseKVDB
# interface.  This class uses the YAML config file to determine
# the database class type.
DB_TYPE = get_db_class()


@router.patch(
    "/devices/{device_id}/edges/weights/",
    tags=[Tag.weights],
    status_code=status.HTTP_200_OK,
)
def set_edges_weights(
    device_id: str,
    session_id: str,
    weights: SetEdgesWeightsRequest,
    response: Response,
):
    with DB_TYPE() as db:
        try:
            device: Device = validate_session_and_device(
                db=db,
                session_id=session_id,
                device_id=device_id,
                response=response,
            )
        except SessionDeviceError as e:
            return {"error": str(e)}

    # Check edge_ids against list of edges on actual device
    extra = set(weights.edge_ids).difference(set(device.model.edge_ids))
    if extra:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": "Invalid edge_ids specified for device " f"{device_id}: {extra}"
        }

    # Set weight of specified edges
    for edge_id in weights.edge_ids:
        driver = EdgeDriver(edge_id)
        driver.set_memory(weights.value)

    result = SetEdgesWeightsResponse(
        device_id=device_id,
        weights=weights,
    )

    return result.model_dump_json()
