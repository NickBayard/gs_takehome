from enum import StrEnum
from fastapi import (
    Response,
    status,
)
from greatsky.db import BaseKVDB
from greatsky.db.orm import (
    Session,
    Device,
)


class Tag(StrEnum):
    devices = "Devices"
    sessions = "Sessions"
    users = "Users"
    currents = "Currents"
    waveforms = "Waveforms"
    weights = "Weights"


class SessionDeviceError(Exception):
    pass


def validate_session_and_device(
   db: BaseDVDB,
   session_id: str,
   device_id: str,
   response: Response, 
) -> Device:
    # check session
    try:
        session = Session.get(session_id, db)
    except KeyError as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise SessionDeviceError(f'Session not found: {session_id}')

    if not session.model.active:
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise SessionDeviceError(f'Session not active: {session_id}')

    #check device
    try:
        device = Device.get(device_id, db)
    except KeyError as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise SessionDeviceError(f'Device not found: {device_id}')

    if device.model.active_session_id != session_id:
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise SessionDeviceError(f'Specified device {device_id} not allocated to session: {session_id}')
    
    return device