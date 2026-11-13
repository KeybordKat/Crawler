from abc import ABC, abstractmethod
from crawler.core.errors import HardwareError

class Legs(ABC):
    """Abstract base class for legs"""
    @abstractmethod
    def stand(self):
        """Stand up"""
        pass

    @abstractmethod
    def sit(self):
        """Sit down"""
        pass

class MockLegs(Legs):
    """Mock legs for testing"""
    def __init__(self, fail=False):
        self.actions = []
        self.fail = fail

    def stand(self):
        """Stand up"""
        if self.fail:
            raise HardwareError("legs failed")
        self.actions.append("stand")

    def sit(self):
        if self.fail:
            raise HardwareError("legs failed")
        self.actions.append("sit")