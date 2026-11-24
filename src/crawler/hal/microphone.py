#imports
from abc import ABC, abstractmethod
from crawler.core.errors import HardwareError

class Microphone(ABC):
    """Abstract base class for microphone sensors"""
    @abstractmethod
    def record(self, seconds):
        """Record audio"""
        pass

    def _check_request(self, seconds):
        """helper method to check general rules for microphone requests"""
        #Check because true counts as 1 in python
        if isinstance(seconds, bool):
            raise ValueError("seconds must be an number")
        if not isinstance(seconds, (int, float)):
            raise ValueError("seconds must be an number")
        if seconds > 60 or seconds <= 0:
            raise ValueError("seconds must be less than or equal to 60 and greater than 0")

class MockMicrophone(Microphone):
    """Mock microphone for testing"""
    def __init__(self, fail=False):
        self.fail = fail

    def record(self, seconds):
        self._check_request(seconds)
        if self.fail:
            raise HardwareError("microphone failed to record")
        return b"mock audio"