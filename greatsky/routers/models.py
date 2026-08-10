from enum import StrEnum
from pydantic import BaseModel, Field, ConfigDict


class Waveform(BaseModel):
    offset: float
    amplitude: float
    frequency: float
    model_config = ConfigDict(extra='forbid')


class WaveformInputModel(BaseModel):
    waveform: Waveform
    # Default input_ids = [] means ALL inputs
    input_ids: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra='forbid')


class WaveformActiveInputModel(BaseModel):
    enabled: bool = False
    # Default input_ids = [] means ALL inputs
    input_ids: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra='forbid')



class WaveformCaptureStatus(StrEnum):
    capturing = 'capturing'
    holding = 'holding'  # not capturing

    
class WaveformStatusOutputModel(BaseModel):
    status: WaveformCaptureStatus = WaveformCaptureStatus.holding
    # Default output_ids = [] means ALL outputs
    output_ids: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra='forbid')


class WaveformCaptureOutput(BaseModel):
    device_id: str
    captures: dict[str, bytearray]
    model_config = ConfigDict(extra='forbid')


class CurrentOutputsModel(BaseModel):
    value: float  # current mA
    enabled: bool = False
    # Default output_ids = [] means ALL outputs
    output_ids: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra='forbid')


class CurrentEdgesModel(BaseModel):
    value: float  # current mA
    enabled: bool = False
    # Default edge_ids = [] means ALL edges
    edge_ids: list[tuple[str, str]] = Field(default_factory=list)
    model_config = ConfigDict(extra='forbid')


class WeightEdgesModel(BaseModel):
    weight: float
    # Default edge_ids = [] means ALL edges
    edge_ids: list[tuple[str, str]] = Field(default_factory=list)
    model_config = ConfigDict(extra='forbid')