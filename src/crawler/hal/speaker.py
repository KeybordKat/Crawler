#imports
from abc import ABC, abstractmethod
from crawler.core.errors import HardwareError

class Speaker(ABC):
    @abstractmethod
    def speak(self, text):
        """speak text"""
        pass

    def _check_request(self, text):
        """helper method to check general rules for speak requests"""
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        if text.strip() == "":
            raise ValueError("Text cannot be empty")

class MockSpeaker(Speaker):
    def __init__(self, fail=False):
        self.spoken = []
        self.fail = fail

    def speak(self, text):
        self._check_request(text)
        if self.fail:
            raise HardwareError("Speaker failure")
        self.spoken.append(text)