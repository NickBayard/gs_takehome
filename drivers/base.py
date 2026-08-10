"""
This module contains the abstraction layer between API handlers that
need to instrument device components (e.g. inputs, outputs, edges).

As there are different device types that support different components
of the instrumentation API, I'm using a driver plugin mechanism for
Input/Output/EdgeDriver classes.  Each of these classes only needs a
portion of the instrumentation API, so we use a combination of the
facade and flyweight design patterns to let each Input/Output/EdgeDriver
class to only have access to the instrumentation drivers that it needs
and only exposes the instrumentation API methods that are appropriate
for that component type.
"""
from greatsky.drivers.lib import (
    poll_driver,
    DriverAttribute,
) 
from greatsky.routers.models import Waveform


class InstrumentError(Exception):
    pass


class BiasDriver:
    def __init__(self, bias_driver):
        self.bias_driver = bias_driver

    def set_voltage(self, value: float):
        assert hasattr(self.bias_driver, 'set_volt')
        self.bias_driver.set_volt(value)

    def get_volt(self) -> float:
        if not hasattr(self.bias_driver, 'get_volt'):
            # not all instrumentation drivers support get_volt
            # we'll raise to let the caller know that it isn't supported
            raise InstrumentError(
                f'Driver {self.bias_driver.__class__.__name__} has '
                'no method get_volt.'
            )
                
    def set_volt_enabled(self, enabled: bool):
        # NOTE: unstable driver interface
        if hasattr(self.bias_driver, 'output_on'):
            if enabled:
                self.bias_driver.output_on()
            else:
                self.bias_driver.output_off()
        else:
            assert hasattr(self.bias_driver, 'output')
            self.bias_driver.output(setting=enabled)

            
class WaveformOutDriver:
    def __init__(self, waveform_driver):
        self.waveform_driver = waveform_driver

    def capture_waveform(self):
        assert hasattr(self.waveform_driver, 'capture_waveform')
        self.waveform_driver.capture_waveform()

    def get_waveform(self) -> bytearray:
        assert hasattr(self.waveform_driver, 'get_waveform')
        return self.waveform_driver.get_waveform()


class WaveformInDriver:
    def __init__(self, waveform_in_driver):
        self.waveform_in_driver = waveform_in_driver

    def set_waveform(self, wave: Waveform):
        assert hasattr(self.waveform_in_driver, 'set_waveform')
        self.waveform_in_driver.set_waveform(wave)

    def set_waveform_enabled(self, enabled: bool):
        # NOTE: unstable driver interface
        if hasattr(self.waveform_in_driver, 'output_on'):
            if enabled:
                self.waveform_in_driver.output_on()
            else:
                self.waveform_in_driver.output_off()
        else:
            assert hasattr(self.waveform_in_driver, 'output')
            self.waveform_in_driver.output(setting=enabled)


class MemoryDriver:
    def __init__(self, memory_driver):
        self.memory_driver = memory_driver
    
    def set_memory(self, value: float):
        assert hasattr(self.memory_driver, 'set_memory')
        self.memory_driver.set_memory(value)


class InputDriver(WaveformInDriver):
    def __init__(self, input_id: str):
        self.input_id = input_id
        WaveformInDriver.__init__(self, poll_driver(DriverAttribute.INPUT_WAVEFORM))

    
class OutputDriver(BiasDriver, WaveformOutDriver):
    def __init__(self, output_id: str):
        self.output_id = output_id
        BiasDriver.__init__(self, poll_driver(DriverAttribute.OUTPUT_BIAS))
        WaveformOutDriver.__init__(self, poll_driver(DriverAttribute.OUTPUT_WAVEFORM))


class EdgeDriver(BiasDriver, MemoryDriver):
    def __init__(self, edge_id: str):
        self.edge_id = edge_id
        BiasDriver.__init__(self, poll_driver(DriverAttribute.EDGE_BIAS))
        MemoryDriver.__init__(self, poll_driver(DriverAttribute.EDGE_WEIGHT))