#imports

#ABC = abstract base class. Used to make sure we don't make a class that doesn't have the right methods
from abc import ABC, abstractmethod

from crawler.core.errors import HardwareError


class Battery(ABC):
    """Abstract base class for battery sensors"""
    @abstractmethod
    def read_voltage(self):
        """Reads the voltage from the sensor"""
        pass

class MockBattery(Battery):
    """Mock battery for testing"""
    def __init__(self, voltage, fail=False):
        self.voltage = voltage
        self.fail = fail

    def read_voltage(self):
        """Returns the voltage it was given in the constructor or raises an error if told to"""
        if self.fail:
            raise HardwareError("battery read failed")
        return self.voltage