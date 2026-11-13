#imports
from crawler.core.errors import HardwareError
#ABC = abstract base class. Used to make sure we don't make a class that doesn't have the right methods
from abc import ABC, abstractmethod

class Distance(ABC):
    """Abstract base class for distance sensors"""
    @abstractmethod
    def read(self):
        """Reads the distance from the sensor"""
        pass

class MockDistance(Distance):
    """Fake distance sensor for testing"""
    def __init__(self, distance_cm, fail=False):
        self.distance_cm = distance_cm
        self.fail = fail

    def read(self):
        """Returns the distance it was given in the constructor or raises an error if told to"""
        if self.fail:
            raise HardwareError("distance sensor timeout")
        return self.distance_cm