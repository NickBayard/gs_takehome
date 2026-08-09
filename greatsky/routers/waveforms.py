from fastapi import (
    APIRouter,
    Response,
    status,
)
from greatsky.db import get_db_class
from greatsky.db.orm import Device
from greatsky.routers.models import (
    WaveformInputModel,
    WaveformActiveInputModel,
    WaveformStatusOutputModel,
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


@router.post(
    "/devices/{device_id}/inputs/waveforms/",
    tags=[Tag.waveforms],
    status_code=status.HTTP_201_CREATED,
)
def create_input_waveforms(
    device_id: str,
    session_id: str,
    wave: WaveformInputModel, 
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
        # TODO create the waveform and associate it will each of the inputs
        # specified for this device.  Then dispatch waveform to drivers.
        # check input_ids against list of inputs on actual device
        
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {'error': 'Not implemented'}


@router.patch(
    "/devices/{device_id}/inputs/waveforms/",
    tags=[Tag.waveforms],
    status_code=status.HTTP_200_OK,
)
def set_input_waveform_activation(
    device_id: str,
    session_id: str,
    activations: WaveformActiveInputModel, 
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
        # TODO check input_ids against list of inputs on actual device
        # activate/dactivte specified inputs on this device
        
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {'error': 'Not implemented'}


@router.patch(
    "/devices/{device_id}/outputs/waveforms/",
    tags=[Tag.waveforms],
    status_code=status.HTTP_200_OK,
)
def set_output_waveform_capture_status(
    device_id: str,
    session_id: str,
    capture: WaveformStatusOutputModel,
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
        # set capture status for specified outputs
        
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {'error': 'Not implemented'}


@router.get(
    "/devices/{device_id}/outputs/waveforms/",
    tags=[Tag.waveforms],
    status_code=status.HTTP_200_OK,
)
def get_output_waveforms(
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
        # collect capture status for specified outputs
        
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {'error': 'Not implemented'}