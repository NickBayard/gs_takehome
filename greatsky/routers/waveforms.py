import json
from fastapi import (
    APIRouter,
    Response,
    status,
)
from greatsky.db import get_db_class
from greatsky.db.orm import Device
from greatsky.drivers.base import InputDriver, OutputDriver
from greatsky.routers.models import (
    WaveformInputModel,
    WaveformActiveInputModel,
    WaveformStatusOutputModel,
    WaveformCaptureStatus,
    WaveformCaptureOutput,
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

    # check input_ids against list of inputs on actual device
    extra = set(wave.input_ids).difference(set(device.model.input_ids))
    if extra:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'error': 'Invalid input_ids specified for device '
                        f'{device_id}: {extra}'
        }
    
    # Dispatch waveform to driver for each of the specified device inputs
    # NOTE: This is highly error prone and wouldn't likely work in the
    # real world.  Several inputs could be conneted to the same waveform
    # generator, which would configure that generator output multiple time.
    # This could realistically take a long time, longer than we want for a
    # synchronous response.
    for input_id in wave.input_ids:
        driver = InputDriver(input_id)
        driver.set_waveform(wave.waveform)
        
    result = dict(
        wave=wave.model.dump(),
        device_id=device_id,
    )

    return json.dumps(result)


@router.patch(
    "/devices/{device_id}/inputs/waveforms/",
    tags=[Tag.waveforms],
    status_code=status.HTTP_200_OK,
)
def set_input_waveform_activation(
    device_id: str,
    session_id: str,
    activation: WaveformActiveInputModel, 
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

    # Check input_ids against list of inputs on actual device
    extra = set(activation.input_ids).difference(set(device.model.input_ids))
    if extra:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'error': 'Invalid input_ids specified for device '
                        f'{device_id}: {extra}'
        }

    # activate/deactivate specified inputs on this device
    for input_id in activation.input_ids:
        driver = InputDriver(input_id)
        driver.set_waveform_enabled(activation.enabled)
        
    result = dict(
        activation=activation.model.dump(),
        device_id=device_id,
    )

    return json.dumps(result)


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

    # Check output_ids against list of outputs on actual device
    extra = set(capture.output_ids).difference(set(device.model.output_ids))
    if extra:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'error': 'Invalid output_ids specified for device '
                     f'{device_id}: {extra}'
        }

    # set capture status for specified outputs
    # NOTE: This highlights an inconsistency in the device API.
    # There's no mechanism to stop capturing.  The assumption is
    # that a get_waveform call will stop capturing and return the
    # captured waveform
    if capture.status == WaveformCaptureStatus.capturing:
        for output_id in capture.output_ids:
            driver = OutputDriver(output_id)
            driver.capture_waveform()
        
    result = dict(
        activation=capture.model.dump(),
        device_id=device_id,
    )

    return json.dumps(result)


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

    # Check output_ids against list of outputs on actual device
    extra = set(output_ids).difference(set(device.model.output_ids))
    if extra:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'error': 'Invalid output_ids specified for device '
                     f'{device_id}: {extra}'
        }

    # collect waveform captures for specified outputs
    captures = {}
    for output_id in output_ids:
        driver = OutputDriver(output_id)
        capture = driver.get_waveform()
        captures[output_id] = capture

    capture = WaveformCaptureOutput(
        device_id=device_id,
        captures=captures,
    )
        
    return capture.model_dump_json()