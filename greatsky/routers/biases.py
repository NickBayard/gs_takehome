from fastapi import (
    APIRouter,
    Response,
    status,
)
from greatsky.db import get_db_class
from greatsky.db.orm import Device
from greatsky.drivers.base import (
    EdgeDriver,
    OutputDriver,
    InstrumentError,
)
from greatsky.routers.models import (
    SetOutputBiasesRequest,
    SetOutputBiasesResponse,
    GetOutputBiasesResponse,
    SetEdgesBiasesRequest,
    SetEdgesBiasesResponse,
    GetEdgesBiasesResponse,
    GetAllBiasesResponse,
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
    "/devices/{device_id}/outputs/biases/",
    tags=[Tag.biases],
    status_code=status.HTTP_200_OK,
)
def set_output_biases(
    device_id: str,
    session_id: str,
    bias: SetOutputBiasesRequest, 
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
    extra = set(bias.output_ids).difference(set(device.model.output_ids))
    if extra:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'error': 'Invalid output_ids specified for device '
                     f'{device_id}: {extra}'
        }

    # Set bias and/or enabled status of specified outputs
    for output_id in bias.output_ids:
        driver = OutputDriver(output_id)
        if bias.value is not None:
            driver.set_voltage(bias.value)
        if bias.enabled is not None:
            driver.set_volt_enabled(bias.enabled)
        
    result = SetOutputBiasesResponse(
        device_id=device_id,
        bias=bias,
    )

    return result.model_dump_json()


@router.get(
    "/devices/{device_id}/outputs/biases/",
    tags=[Tag.biases],
    status_code=status.HTTP_200_OK,
)
def get_output_biases(
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

    # Get bias and enabled status of specified outputs
    errors = []
    biases = {}
    for output_id in output_ids:
        driver = OutputDriver(output_id)
        try:
            biases[output_id] = driver.get_volt()
        except InstrumentError as e:
            errors.append(f'Output_id {output_id}: str(e)')
        
    result = GetOutputBiasesResponse(
        device_id=device_id,
        biases=biases,
        errors=errors,
    )

    return result.model_dump_json()


@router.patch(
    "/devices/{device_id}/edges/biases/",
    tags=[Tag.biases],
    status_code=status.HTTP_200_OK,
)
def set_edges_biases(
    device_id: str,
    session_id: str,
    biases: SetEdgesBiasesRequest, 
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

    # Check edge_ids against list of edges on actual device
    extra = set(biases.edge_ids).difference(set(device.model.edge_ids))
    if extra:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'error': 'Invalid edge_ids specified for device '
                     f'{device_id}: {extra}'
        }

    # Set bias and/or enabled status of specified outputs
    for edge_id in biases.edge_ids:
        driver = EdgeDriver(edge_id)
        if biases.value is not None:
            driver.set_voltage(biases.value)
        if biases.enabled is not None:
            driver.set_volt_enabled(biases.enabled)
        
    result = SetEdgesBiasesResponse(
        device_id=device_id,
        biases=biases,
    )

    return result.model_dump_json()


@router.get(
    "/devices/{device_id}/edges/biases/",
    tags=[Tag.biases],
    status_code=status.HTTP_200_OK,
)
def get_edge_biases(
    device_id: str,
    session_id: str,
    edge_ids: list[tuple[str, str]], 
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

    # Check edge_ids against list of edges on actual device
    extra = set(edge_ids).difference(set(device.model.edge_ids))
    if extra:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'error': 'Invalid edge_ids specified for device '
                     f'{device_id}: {extra}'
        }

    # Gete bias values of specified edges
    errors = []
    biases = {}
    for edge_id in edge_ids:
        driver = EdgeDriver(edge_id)
        try:
            biases[edge_id] = driver.get_volt()
        except InstrumentError as e:
            errors.append(f'Edge_id {edge_id}: str(e)')
        
    result = GetEdgesBiasesResponse(
        device_id=device_id,
        biases=biases,
        errors=errors,
    )

    return result.model_dump_json()


@router.patch(
    "/devices/{device_id}/biases/",
    tags=[Tag.biases],
    status_code=status.HTTP_200_OK,
)
def get_all_biases(
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

    # Get biases of all outputs and edges
    errors = []
    edge_biases = {}
    for edge_id in device.model.edge_ids:
        driver = EdgeDriver(edge_id)
        try:
            edge_biases[edge_id] = driver.get_volt()
        except InstrumentError as e:
            errors.append(f'Edge_id {edge_id}: str(e)')

    output_biases = {}
    for output_id in device.model.output_ids:
        driver = OutputDriver(output_id)
        try:
            output_biases[output_id] = driver.get_volt()
        except InstrumentError as e:
            errors.append(f'Output_id {output_id}: str(e)')
        
    result = GetAllBiasesResponse(
        device_id=device_id,
        output_biases=output_biases,
        edge_biases=edge_biases,
        errors=errors,
    )

    return result.model_dump_json()