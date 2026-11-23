#imports
from abc import ABC, abstractmethod

from crawler.core.errors import HardwareError


class Camera(ABC):

    @abstractmethod
    def take_photo(self):
        """Take a photo"""
        pass

class MockCamera(Camera):

    def __init__(self, fail=False):
        self.fail = fail

    def take_photo(self):
        if self.fail:
            raise HardwareError("camera failure")
        return b"mock photo"