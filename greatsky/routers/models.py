from enum import StrEnum
from pydantic import BaseModel, Field, ConfigDict


class Waveform(BaseModel):
    offset: float
    amplitude: float
    frequency: float
    model_config = ConfigDict(extra="forbid")


class CreateInputWaveformsRequest(BaseModel):
    waveform: Waveform
    # Default input_ids = [] means ALL inputs
    input_ids: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


class CreateInputWaveformsResponse(BaseModel):
    device_id: str
    wave: CreateInputWaveformsRequest
    model_config = ConfigDict(extra="forbid")


class SetInputWaveformActivationRequest(BaseModel):
    enabled: bool = False
    # Default input_ids = [] means ALL inputs
    input_ids: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


class SetInputWaveformActivationResponse(BaseModel):
    device_id: str
    activation: SetInputWaveformActivationRequest
    model_config = ConfigDict(extra="forbid")


class WaveformCaptureStatus(StrEnum):
    capturing = "capturing"
    holding = "holding"  # not capturing


class SetOutputWaveformCaptureStatusRequest(BaseModel):
    status: WaveformCaptureStatus = WaveformCaptureStatus.holding
    # Default output_ids = [] means ALL outputs
    output_ids: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


class SetOutputWaveformCaptureStatusResponse(BaseModel):
    device_id: str
    capture: SetOutputWaveformCaptureStatusRequest
    model_config = ConfigDict(extra="forbid")


class GetOutputWaveformsResponse(BaseModel):
    device_id: str
    captures: dict[str, bytes]
    model_config = ConfigDict(extra="forbid")


class SetOutputBiasesRequest(BaseModel):
    # For value and enabled, None means don't change the setting
    value: float | None = None  # voltage V
    enabled: bool | None = None
    # Default output_ids = [] means ALL outputs
    output_ids: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


class SetOutputBiasesResponse(BaseModel):
    device_id: str
    bias: SetOutputBiasesRequest
    model_config = ConfigDict(extra="forbid")


class GetOutputBiasesResponse(BaseModel):
    device_id: str
    # biases is a dict of output_ids to voltages
    biases: dict[str, float] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


class SetEdgesBiasesRequest(BaseModel):
    value: float | None = None
    enabled: bool | None = None
    # Default edge_ids = [] means ALL edges
    edge_ids: list[tuple[str, str]] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


class SetEdgesBiasesResponse(BaseModel):
    device_id: str
    biases: SetEdgesBiasesRequest
    model_config = ConfigDict(extra="forbid")


class GetEdgesBiasesResponse(BaseModel):
    device_id: str
    # biases is a dict of output_ids to voltages
    biases: dict[tuple[str, str], float] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


class GetAllBiasesResponse(BaseModel):
    device_id: str
    output_biases: dict[str, float] = Field(default_factory=dict)
    edge_biases: dict[tuple[str, str], float] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


class SetEdgesWeightsRequest(BaseModel):
    weight: float
    # Default edge_ids = [] means ALL edges
    edge_ids: list[tuple[str, str]] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


class SetEdgesWeightsResponse(BaseModel):
    device_id: str
    weights: SetEdgesWeightsRequest
    model_config = ConfigDict(extra="forbid")
