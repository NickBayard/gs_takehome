import json
import random
from fastapi import (
    APIRouter,
    Response,
    status,
)
from greatsky.db import get_db_class
from greatsky.db.orm import (
    Device,
    Session,
    SessionModel,
)
from greatsky.utils import Tag


router = APIRouter()

# get_db_class allows us to swap out another key-value data store
# provided that a facade has been created to follow the BaseKVDB
# interface.  This class uses the YAML config file to determine
# the database class type.
DB_TYPE = get_db_class()


@router.post(
    "/devices/{device_id}/sessions/",
    tags=[Tag.sessions],
    status_code=status.HTTP_201_CREATED,
)
def create_device_session(device_id: str, response: Response):
    """
    Create a new session for a specific device
    """
    with DB_TYPE() as db:
        try:
            device = Device.get(device_id, db)
        except KeyError as e:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'error': f'Device not found: {device_id}'}
            
        if device.model.active_session_id:
            response.status_code = status.HTTP_409_CONFLICT
            return {'error': 'Device is currently locked in another'
                    f'session: {device_id}'}

        # create a new session
        session = Session(
            model=SessionModel(
                device_id=device_id,
                active=True,
            ) 
        )
        
        # associate session with this device
        device.model.active_session_id = session.db_id

        # persist session and device
        session.update(db)
        device.update(db)
        return session.model_dump_json()


@router.post(
    "/devices/sessions/",
    tags=[Tag.sessions],
    status_code=status.HTTP_201_CREATED,
)
def create_session(response: Response):
    """
    Create a new session for any device
    """
    with DB_TYPE() as db:
        # Allocate any device
        devices = Device.get_all(db)
        # prevent the same device from being selected for each new run
        random.shuffle(devices)

        for device in devices:
            if not device.model.active_session_id:
                # found a free device
                break
        else:  # no free devices
            response.status_code = status.HTTP_409_CONFLICT
            return {'error': 'All devices are currently locked other sessions'}

        # create a new session
        session = Session(
            model=SessionModel(
                device_id=device_id,
                active=True,
            ) 
        )
        # associate session with this device
        device.model.active_session_id = session.db_id

        # persist session and device
        session.update(db)
        device.update(db)
        return session.model_dump_json()

        
@router.get(
    "/devices/sessions/{session_id}",
    tags=[Tag.sessions],
    status_code=status.HTTP_200_OK,
)
def get_session(session_id: str, response: Response):
    """
    Get a specific session.
    """
    with DB_TYPE() as db:
        try:
            session = Session.get(session_id, db)
        except KeyError as e:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'error': f'Session not found: {session_id}'}
        
        return session.model_dump_json()


@router.get(
    "/devices/sessions/",
    tags=[Tag.sessions],
    status_code=status.HTTP_200_OK,
)
def get_all_sessions():
    """
    Get a specific session.
    """
    with DB_TYPE() as db:
        sessions = Session.get_all(db)

    return {'sessions': [
        session.model_dump_json() for session in sessions
    ]}


@router.patch(
    "/devices/sessions/{session_id}",
    tags=[Tag.sessions],
    status_code=status.HTTP_200_OK,
)
def deactivate_session(session_id: str, response: Response):
    """
    Deactivate a session.  Does not delete from the database
    """
    with DB_TYPE() as db:
        try:
            session = Session.get(session_id, db)
        except KeyError as e:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'error': f'Session not found: {session_id}'}
        
        error = None
        try:
            device = Device.get(session.model.device_id, db)
        except KeyError:
            # We will still close the session and only send an error message
            # with the body.
            error = f'Device not found for session. Ignored.'

        session.model.active = False
        session.update(db)
        if not error:
            device.model.active_session_id = None
            device.update(db)
        
        result = session.model_dump()
        if error:
            result['error'] = error
        return json.dumps(result)