from fastapi import (
    APIRouter,
    Response,
    status,
)
from greatsky.db import get_db_class
from greatsky.db.orm import Device
from greatsky.routers.models import (
    CurrentOutputsModel,
    CurrentEdgesModel,
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
    "/devices/{device_id}/outputs/currents/",
    tags=[Tag.currents],
    status_code=status.HTTP_200_OK,
)
def set_output_currents(
    device_id: str,
    session_id: str,
    settings: CurrentOutputsModel, 
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
            return {'error': str(e)}

        # Device and session are active
        # TODO check output_ids against list of outputs on actual device
        # Set current and/or enabled status of specified outputs
        
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {'error': 'Not implemented'}


@router.get(
    "/devices/{device_id}/outputs/currents/",
    tags=[Tag.currents],
    status_code=status.HTTP_200_OK,
)
def get_output_currents(
    device_id: str,
    session_id: str,
    output_ids: list[str], 
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
            return {'error': str(e)}

        # Device and session are active
        # TODO check output_ids against list of outputs on actual device
        # Get current and enabled status of specified outputs
        
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {'error': 'Not implemented'}


@router.patch(
    "/devices/{device_id}/edges/currents/",
    tags=[Tag.currents],
    status_code=status.HTTP_200_OK,
)
def set_edges_currents(
    device_id: str,
    session_id: str,
    settings: CurrentEdgesModel, 
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
            return {'error': str(e)}

        # Device and session are active
        # TODO check edge_ids against list of edges on actual device
        # Set current and/or enabled status of specified outputs
        
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {'error': 'Not implemented'}


@router.get(
    "/devices/{device_id}/edges/currents/",
    tags=[Tag.currents],
    status_code=status.HTTP_200_OK,
)
def get_edge_currents(
    device_id: str,
    session_id: str,
    edge_ids: list[str], 
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
            return {'error': str(e)}

        # Device and session are active
        # TODO check edge_ids against list of edges on actual device
        # Get current and enabled status of specified edges
        
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {'error': 'Not implemented'}



@router.patch(
    "/devices/{device_id}/currents/",
    tags=[Tag.currents],
    status_code=status.HTTP_200_OK,
)
def get_all_currents(
    device_id: str,
    session_id: str,
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
            return {'error': str(e)}

        # Device and session are active
        # Set current and/or enabled status of all outputs and edges
        
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {'error': 'Not implemented'}