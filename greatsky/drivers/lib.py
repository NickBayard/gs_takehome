import random
from enum import Enum, auto
from typing import Any

from greatsky.routers.models import Waveform


class VoltageSource:
    """
    This is a driver class for an instrument which connect to a single
    device's bias connection
    """

    def output(self, setting: bool):
        # Function which turns output of the instrument on or off
        pass

    def set_volt(self, value: float):
        # Function which sets the voltage level the instrument will output
        # when turned on
        pass

    def get_volt(self) -> float:
        # Function which returns voltage level the instrument will output
        # when turned on
        return random.uniform(0.0, 10.0)

    def set_memory(self, value: float):
        #  Function which sets the memory of an edge if connected to an
        # edge's memory
        pass


class RFSoC:
    """
    This is a driver class for an instrument which is used to send and
    receive analog waveforms
    """

    def set_waveform(self, wave: Waveform):
        # Writes <wave> to the memory of the RFSoC
        pass

    def capture_waveform(self):
        # Reads input from analog to digital (ADC) of the RFSoC and stores
        # the waveform in the memory of the RFSoC
        pass

    def get_waveform(self) -> bytearray:
        # Returns the stored waveform in the memory of the RFSoC
        return bytearray(random.randbytes(100))

    def output_on(self):
        # Outputs the waveform stored in the memory of the RFSoC
        pass

    def output_off(self):
        # Turns off the output of the RFSoC
        pass


class AWG:
    """
    This is a driver class for an AWG "arbitrary waveform generator", which
    is used to send analog waveforms
    """

    def set_volt(self, value: float):
        # Function which sets the voltage level the instrument will output
        # when turned on
        pass

    def set_waveform(self, wave: Waveform):
        # Writes <wave> to the memory of the AWG
        pass

    def output_on(self):
        # Outputs the waveform stored in the memory of the AWG
        pass

    def output_off(self):
        # Turns off the output of the AWG
        pass


class Scope:
    """
    This is a driver class for a oscilloscope. which is used to capture
    analog waveforms
    """

    def capture_waveform(self):
        # Reads input from analog to digital (ADC) of the scope and stores
        # the waveform in the memory of the scope
        pass

    def get_waveform(self) -> bytearray:
        # Returns the stored waveform in the memory of the scope
        return bytearray(random.randbytes(100))


class MemoryController:
    """
    This is a driver class for a instrument which connects to multiple edge's
    memory at the same time.
    """

    def set_memory(self, value: float, row: int, col: int):
        # This function sets the memory for an edge for indexed by the
        # edge's adjacency matrix row and column.
        pass


class DriverAttribute(Enum):
    EDGE_BIAS = auto()
    EDGE_WEIGHT = auto()
    OUTPUT_BIAS = auto()
    OUTPUT_WAVEFORM = auto()
    INPUT_WAVEFORM = auto()


# Realistically the attribute type wouldn't be mapped to a specific
# driver class.  It would be dependent on the configuration for each
# device.  This configuratio "should" be part of the POST /devices API,
# but the assignment requires the use of poll_driver.  So we are just
# mocking things for now.
_DRIVER_ATTRIBUTE_MAP: dict[DriverAttribute, Any] = {
    DriverAttribute.EDGE_BIAS: VoltageSource,
    DriverAttribute.EDGE_WEIGHT: MemoryController,
    DriverAttribute.OUTPUT_BIAS: VoltageSource,
    DriverAttribute.OUTPUT_WAVEFORM: Scope,
    DriverAttribute.INPUT_WAVEFORM: AWG,
}


def poll_driver(
    attribute: DriverAttribute,
) -> VoltageSource | RFSoC | AWG | Scope | MemoryController:
    """
    This function polls the physical system and returns a
    driver class for the provided attribute. Examples of an attribute are edge-bias,
    edge-weight, output-bias... ect.
    """

    # NOTE: poll_driver should also specify the specific node or edge
    # in order to ensure the correct driver is dispatched.  We are just going to
    # pretend that the correct instance is being distributed.
    return _DRIVER_ATTRIBUTE_MAP[attribute].value()
